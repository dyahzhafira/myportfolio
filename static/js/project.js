// getCookie & escapeHtml dimuat dari static/js/common.js (lihat base.html)
(function () {
    const loadingState = document.getElementById('loading');
    const errorState = document.getElementById('error');
    const emptyState = document.getElementById('empty');
    const gridContainer = document.getElementById('grid');
    const searchForm = document.getElementById('project-search-form');
    const searchInput = document.getElementById('search-input');
    const projectForm = document.getElementById('project-form');

    // Elemen bisa null kalau script ini kebawa load di halaman lain, jadi hentikan
    // eksekusi di sini supaya querySelector di bawah tidak melempar error di tengah jalan.
    if (!gridContainer) return;

    const SEARCH_DEBOUNCE_DELAY = 300;
    let searchDebounceTimer;
    let projectsAbortController;

    function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
        loadingState.classList.toggle('hide', !showLoading);
        errorState.classList.toggle('hide', !showError);
        emptyState.classList.toggle('hide', !showEmpty);
        gridContainer.classList.toggle('hide', !showGrid);
    }

    function buildProjectCardElement(item) {
        const project = item.fields;
        const projectId = item.id;
        const slug = item.slug;

        const articleElement = document.createElement('article');
        articleElement.className = 'project-card';

        const imageHtml = project.project_image_url
            ? `<img src="${escapeHtml(project.project_image_url)}" alt="Gambar ${escapeHtml(project.title)}" class="project-image">`
            : '';

        const techStackHtml = (project.tech_stack || [])
            .map((tech) => `<span class="tech-badge"><img src="https://cdn.simpleicons.org/${escapeHtml(tech.icon)}" alt="" loading="lazy">${escapeHtml(tech.name)}</span>`)
            .join('');

        const detailUrl = DETAIL_URL_TEMPLATE.replace('placeholder-slug', slug);
        const editUrl = EDIT_URL_TEMPLATE.replace('placeholder-slug', slug);
        const deleteUrl = DELETE_URL_TEMPLATE.replace('placeholder-slug', slug);
        const starUrl = STAR_URL_TEMPLATE.replace('00000000-0000-0000-0000-000000000000', projectId);

        const editHtml = IS_EDITOR
            ? `<a href="${editUrl}" class="button">Edit</a>`
            : '';

        // Form hapus ini dikirim lewat navigasi biasa (bukan fetch), jadi Django tetap
        // butuh field csrfmiddlewaretoken di body-nya. {% csrf_token %} tidak bisa
        // dipakai di sini karena markup ini dirakit di berkas .js statis yang tidak
        // diproses Django, jadi nilai cookie csrftoken-nya dipakai langsung sebagai token.
        const deleteHtml = IS_OWNER
            ? `<form method="post" action="${deleteUrl}" style="display:inline;">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                    <button type="submit" class="button button-danger" onclick="return confirm('Yakin ingin menghapus project ini?');">Hapus</button>
               </form>`
            : '';

        const isStarredClass = project.is_starred ? ' is-starred' : '';
        const starText = project.is_starred ? 'Unstar' : 'Star';
        const starTitle = project.star_count > 0
            ? `Dibintangi oleh ${escapeHtml(project.starred_by_names)}`
            : 'Jadilah yang pertama memberi star';

        articleElement.innerHTML = `
            ${imageHtml}
            <span class="project-tag">${escapeHtml(project.project_type_display)} &middot; ${escapeHtml(project.status_display)}</span>
            <h2><a href="${detailUrl}">${escapeHtml(project.title)}</a></h2>
            <p class="project-description">${escapeHtml(project.description)}</p>
            <div class="tech-stack">${techStackHtml}</div>
            <div class="project-card-actions">
                <button type="button"
                        class="button button-star${isStarredClass}"
                        data-star-button
                        data-star-url="${starUrl}"
                        title="${starTitle}">
                    <span aria-hidden="true">&#9733;</span>
                    <span data-star-text>${starText}</span>
                    <span class="star-count" data-star-count>${project.star_count}</span>
                </button>
                ${editHtml}
                ${deleteHtml}
            </div>
        `;

        return articleElement;
    }

    async function fetchProjects(searchQuery = '') {
        // Kalau user mengetik cepat, fetch sebelumnya mungkin belum selesai saat fetch
        // baru dikirim. AbortController membatalkan request lama itu supaya hasil yang
        // lebih dulu kembali dari server tidak menimpa hasil pencarian yang lebih baru.
        if (projectsAbortController) projectsAbortController.abort();
        projectsAbortController = new AbortController();

        try {
            displayPageSection({ showLoading: true });

            const params = new URLSearchParams();
            if (searchQuery) params.set('title', searchQuery);
            if (INITIAL_SORT === 'star') params.set('sort', 'star');

            const url = params.toString() ? `${BASE_PROJECTS_ENDPOINT}?${params.toString()}` : BASE_PROJECTS_ENDPOINT;

            const response = await fetch(url, {
                headers: { 'Accept': 'application/json' },
                signal: projectsAbortController.signal,
            });

            if (!response.ok) throw new Error('Failed to fetch data');

            const projectData = await response.json();

            if (projectData.length === 0) {
                displayPageSection({ showEmpty: true });
            } else {
                gridContainer.innerHTML = '';
                projectData.forEach((item) => {
                    gridContainer.appendChild(buildProjectCardElement(item));
                });
                displayPageSection({ showGrid: true });
            }
        } catch (error) {
            if (error.name === 'AbortError') return;
            console.error('Error loading projects:', error);
            displayPageSection({ showError: true });
        }
    }

    //toggle star lewat AJAX
    gridContainer.addEventListener('click', async function (event) {
        const button = event.target.closest('[data-star-button]');
        if (!button) return;

        button.disabled = true;
        try {
            const response = await fetch(button.dataset.starUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });

            // Cek status duluan sebelum parse body. Pengunjung yang belum pernah
            // dapat cookie CSRF (anonim, tanpa form apa pun yang ter-render) bisa
            // menerima halaman error CSRF bawaan Django, bukan JSON, jadi kita cuma
            // perlu tahu statusnya 403 dan tidak perlu baca isi body itu sama sekali.
            if (response.status === 403) {
                if (typeof showToast === 'function') {
                    showToast('Gagal', 'Silakan login terlebih dahulu untuk memberi star.', 'error');
                }
                return;
            }
            if (!response.ok) throw new Error('Failed to toggle star');

            const result = await response.json();
            button.classList.toggle('is-starred', result.is_starred);
            button.querySelector('[data-star-text]').textContent = result.is_starred ? 'Unstar' : 'Star';
            button.querySelector('[data-star-count]').textContent = result.star_count;
        } catch (error) {
            console.error('Error toggling star:', error);
            if (typeof showToast === 'function') {
                showToast('Gagal', 'Tidak dapat memperbarui star. Silakan coba lagi.', 'error');
            }
        } finally {
            button.disabled = false;
        }
    });

    function searchProjects() {
        fetchProjects(searchInput.value.trim());
    }

    // Debounce: tiap ketikan membatalkan timer sebelumnya dan menjadwal ulang. Request
    // baru dikirim ke server setelah user berhenti mengetik selama SEARCH_DEBOUNCE_DELAY,
    // jadi tidak ada satu request terpisah untuk tiap huruf yang diketik.
    searchInput.addEventListener('input', function () {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(searchProjects, SEARCH_DEBOUNCE_DELAY);
    });

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchProjects();
    });

    //modal tambah proyek via AJAX
    function closeProjectModal() {
        const modal = document.getElementById('add-project-modal');
        if (modal) modal.hidePopover();
    }

    async function addProject(event) {
        event.preventDefault();
        const submitButton = projectForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const response = await fetch(CREATE_PROJECT_ENDPOINT, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: new FormData(projectForm),
            });

            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                projectForm.reset();
                closeProjectModal();
                if (typeof showToast === 'function') {
                    showToast('Berhasil', 'Proyek baru berhasil ditambahkan!', 'success');
                }
                fetchProjects(searchInput.value.trim());
            } else {
                const errorMessages = result.errors
                    ? Object.values(result.errors).flat().map((error) => error.message)
                    : [result.message || `Terjadi kesalahan (status ${response.status}).`];
                if (typeof showToast === 'function') {
                    showToast('Gagal menambahkan proyek', errorMessages.join(' '), 'error');
                }
            }
        } catch (error) {
            console.error('Error adding project:', error);
            if (typeof showToast === 'function') {
                showToast('Gagal menambahkan proyek', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
            }
        } finally {
            submitButton.disabled = false;
        }
    }

    if (projectForm) {
        projectForm.addEventListener('submit', addProject);
    }

    fetchProjects(searchInput.value.trim());
})();
