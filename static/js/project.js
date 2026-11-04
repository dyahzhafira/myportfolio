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
    const ID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';
    let searchDebounceTimer;
    let projectsAbortController;

    function notify(title, message, type) {
        if (typeof showToast === 'function') showToast(title, message, type);
    }

    function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
        loadingState.classList.toggle('hide', !showLoading);
        errorState.classList.toggle('hide', !showError);
        emptyState.classList.toggle('hide', !showEmpty);
        gridContainer.classList.toggle('hide', !showGrid);
    }

    // Kontrak DRF: objek proyek sudah flat (project.title), bukan item.fields.title
    // seperti endpoint JsonResponse lama.
    function buildProjectCardElement(project) {
        const articleElement = document.createElement('article');
        articleElement.className = 'project-card';

        const imageHtml = project.project_image_url
            ? `<img src="${escapeHtml(project.project_image_url)}" alt="Gambar ${escapeHtml(project.title)}" class="project-image">`
            : '';

        const techStackHtml = (project.tech_stack || [])
            .map((tech) => `<span class="tech-badge"><img src="https://cdn.simpleicons.org/${escapeHtml(tech.icon)}" alt="" loading="lazy">${escapeHtml(tech.name)}</span>`)
            .join('');

        const detailUrl = DETAIL_URL_TEMPLATE.replace('placeholder-slug', encodeURIComponent(project.slug));
        const editUrl = EDIT_URL_TEMPLATE.replace('placeholder-slug', encodeURIComponent(project.slug));
        const starUrl = STAR_URL_TEMPLATE.replace(ID_PLACEHOLDER, project.id);

        const editHtml = IS_EDITOR
            ? `<a href="${editUrl}" class="button">Edit</a>`
            : '';

        // Hapus sekarang lewat DELETE ke API (bukan form POST), jadi cukup tombol
        // dengan data-id. Izin sebenarnya tetap dicek server, bukan oleh IS_OWNER.
        const deleteHtml = IS_OWNER
            ? `<button type="button" class="button button-danger" data-delete-button data-id="${escapeHtml(project.id)}">Hapus</button>`
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
                projectData.forEach((project) => {
                    gridContainer.appendChild(buildProjectCardElement(project));
                });
                displayPageSection({ showGrid: true });
            }
        } catch (error) {
            if (error.name === 'AbortError') return;
            console.error('Error loading projects:', error);
            displayPageSection({ showError: true });
        }
    }

    // Error DRF berbentuk {"title": ["..."]} (validasi) atau {"detail": "..."} (izin).
    function apiErrorMessage(data, status) {
        const messages = Object.values(data).flat().filter((value) => typeof value === 'string');
        return messages.join(' ') || `Terjadi kesalahan (status ${status}).`;
    }

    //toggle star lewat API
    gridContainer.addEventListener('click', async function (event) {
        const button = event.target.closest('[data-star-button]');
        if (!button) return;

        button.disabled = true;
        try {
            const response = await fetch(button.dataset.starUrl, {
                method: 'POST',
                headers: { 'Accept': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            });

            // Pengunjung yang belum login mendapat 403 dari permission IsAuthenticated.
            // Cukup cek statusnya, isi body tidak perlu dibaca.
            if (response.status === 403) {
                notify('Gagal', 'Silakan login terlebih dahulu untuk memberi star.', 'error');
                return;
            }
            if (!response.ok) throw new Error('Failed to toggle star');

            const result = await response.json();
            button.classList.toggle('is-starred', result.is_starred);
            button.querySelector('[data-star-text]').textContent = result.is_starred ? 'Unstar' : 'Star';
            button.querySelector('[data-star-count]').textContent = result.star_count;
        } catch (error) {
            console.error('Error toggling star:', error);
            notify('Gagal', 'Tidak dapat memperbarui star. Silakan coba lagi.', 'error');
        } finally {
            button.disabled = false;
        }
    });

    //hapus proyek lewat DELETE
    gridContainer.addEventListener('click', async function (event) {
        const button = event.target.closest('[data-delete-button]');
        if (!button) return;
        if (!window.confirm('Yakin ingin menghapus project ini?')) return;

        button.disabled = true;
        try {
            const response = await fetch(DETAIL_API_TEMPLATE.replace(ID_PLACEHOLDER, button.dataset.id), {
                method: 'DELETE',
                headers: { 'Accept': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            });

            // 204 No Content tidak punya body, jadi .json() tidak boleh dipanggil.
            if (response.status !== 204) {
                const result = await response.json().catch(() => ({}));
                throw new Error(apiErrorMessage(result, response.status));
            }

            notify('Berhasil', 'Proyek berhasil dihapus.', 'success');
            fetchProjects(searchInput.value.trim());
        } catch (error) {
            console.error('Error deleting project:', error);
            notify('Gagal menghapus proyek', error.message, 'error');
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

    //modal tambah proyek via API
    function closeProjectModal() {
        const modal = document.getElementById('add-project-modal');
        if (modal) modal.hidePopover();
    }

    async function addProject(event) {
        event.preventDefault();
        const submitButton = projectForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            // Pilih field secara eksplisit supaya token CSRF di form tidak ikut terkirim.
            const fields = new FormData(projectForm);
            const payload = Object.fromEntries(
                ['title', 'description', 'status', 'project_type', 'project_url', 'project_image_url']
                    .map((name) => [name, fields.get(name)])
            );

            const response = await fetch(BASE_PROJECTS_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                projectForm.reset();
                closeProjectModal();
                notify('Berhasil', 'Proyek baru berhasil ditambahkan!', 'success');
                fetchProjects(searchInput.value.trim());
            } else {
                notify('Gagal menambahkan proyek', apiErrorMessage(result, response.status), 'error');
            }
        } catch (error) {
            console.error('Error adding project:', error);
            notify('Gagal menambahkan proyek', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
        } finally {
            submitButton.disabled = false;
        }
    }

    if (projectForm) {
        projectForm.addEventListener('submit', addProject);
    }

    fetchProjects(searchInput.value.trim());
})();
