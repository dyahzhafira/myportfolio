// getCookie & escapeHtml dimuat dari static/js/common.js (lihat base.html)
(function () {
    const loadingState = document.getElementById('experience-loading');
    const errorState = document.getElementById('experience-error');
    const emptyState = document.getElementById('experience-empty');
    const gridContainer = document.getElementById('experience-grid');
    const searchForm = document.getElementById('experience-search-form');
    const searchInput = document.getElementById('experience-search-input');
    const categoryFilter = document.getElementById('experience-category-filter');
    const sortSelect = document.getElementById('experience-sort');
    const experienceForm = document.getElementById('experience-form');
    const addButton = document.getElementById('experience-add-button');
    const modal = document.getElementById('add-experience-modal');

    // Hentikan eksekusi kalau script kebawa load di halaman lain.
    if (!gridContainer) return;

    const SEARCH_DEBOUNCE_DELAY = 300;
    const ID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';
    const experienceCache = new Map();
    let editingId = null;
    let searchDebounceTimer;
    let experiencesAbortController;

    function notify(title, message, type) {
        if (typeof showToast === 'function') showToast(title, message, type);
    }

    // Error DRF: {"title": ["..."]} (validasi) atau {"detail": "..."} (izin).
    function apiErrorMessage(data, status) {
        const messages = Object.values(data).flat().filter((value) => typeof value === 'string');
        return messages.join(' ') || `Terjadi kesalahan (status ${status}).`;
    }

    // Semua request tulis lewat sini supaya header CSRF dan error konsisten.
    async function writeExperience(url, method, payload) {
        const headers = { 'Accept': 'application/json', 'X-CSRFToken': getCookie('csrftoken') };
        if (payload !== undefined) headers['Content-Type'] = 'application/json';

        const response = await fetch(url, {
            method,
            headers,
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });

        // 204 No Content tidak punya body, jangan panggil .json().
        if (response.status === 204) return null;
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(apiErrorMessage(data, response.status));
        return data;
    }

    function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
        loadingState.classList.toggle('hide', !showLoading);
        errorState.classList.toggle('hide', !showError);
        emptyState.classList.toggle('hide', !showEmpty);
        gridContainer.classList.toggle('hide', !showGrid);
    }

    function buildExperienceCardElement(experience) {
        const articleElement = document.createElement('article');
        articleElement.className = 'project-card';

        const starUrl = EXPERIENCE_STAR_URL_TEMPLATE.replace(ID_PLACEHOLDER, experience.id);
        const isStarredClass = experience.is_starred ? ' is-starred' : '';
        const starText = experience.is_starred ? 'Unstar' : 'Star';
        const starTitle = experience.star_count > 0
            ? `Dibintangi oleh ${escapeHtml(experience.starred_by_names)}`
            : 'Jadilah yang pertama memberi star';
        const statusText = experience.is_ongoing ? 'Sedang berlangsung' : 'Selesai';

        const editHtml = IS_EDITOR_EXPERIENCE
            ? `<button type="button" class="button" data-edit-button data-id="${escapeHtml(experience.id)}">Edit</button>`
            : '';
        const deleteHtml = IS_OWNER_EXPERIENCE
            ? `<button type="button" class="button button-danger" data-delete-button data-id="${escapeHtml(experience.id)}">Hapus</button>`
            : '';

        articleElement.innerHTML = `
            <span class="project-tag">${escapeHtml(experience.category_display)} &middot; ${escapeHtml(statusText)}</span>
            <h2>${escapeHtml(experience.title)}</h2>
            <p class="project-description">${escapeHtml(experience.description)}</p>
            <div class="project-card-actions">
                <button type="button"
                        class="button button-star${isStarredClass}"
                        data-star-button
                        data-star-url="${starUrl}"
                        title="${starTitle}">
                    <span aria-hidden="true">&#9733;</span>
                    <span data-star-text>${starText}</span>
                    <span class="star-count" data-star-count>${experience.star_count}</span>
                </button>
                ${editHtml}
                ${deleteHtml}
            </div>
        `;

        return articleElement;
    }

    async function fetchExperiences() {
        // Batalkan fetch lama supaya hasil yang lambat tidak menimpa hasil terbaru.
        if (experiencesAbortController) experiencesAbortController.abort();
        experiencesAbortController = new AbortController();

        try {
            displayPageSection({ showLoading: true });

            const params = new URLSearchParams();
            const title = searchInput.value.trim();
            if (title) params.set('title', title);
            if (categoryFilter.value) params.set('category', categoryFilter.value);
            if (sortSelect.value) params.set('sort', sortSelect.value);

            const url = params.toString() ? `${EXPERIENCES_ENDPOINT}?${params.toString()}` : EXPERIENCES_ENDPOINT;
            const response = await fetch(url, {
                headers: { 'Accept': 'application/json' },
                signal: experiencesAbortController.signal,
            });

            if (!response.ok) throw new Error('Failed to fetch data');

            const experienceData = await response.json();
            experienceCache.clear();
            experienceData.forEach((experience) => experienceCache.set(experience.id, experience));

            if (experienceData.length === 0) {
                displayPageSection({ showEmpty: true });
            } else {
                gridContainer.innerHTML = '';
                experienceData.forEach((experience) => {
                    gridContainer.appendChild(buildExperienceCardElement(experience));
                });
                displayPageSection({ showGrid: true });
            }
        } catch (error) {
            if (error.name === 'AbortError') return;
            console.error('Error loading experiences:', error);
            displayPageSection({ showError: true });
        }
    }

    // Satu handler klik untuk star, edit, dan hapus (event delegation).
    gridContainer.addEventListener('click', async function (event) {
        const starButton = event.target.closest('[data-star-button]');
        const editButton = event.target.closest('[data-edit-button]');
        const deleteButton = event.target.closest('[data-delete-button]');

        if (starButton) {
            starButton.disabled = true;
            try {
                const result = await writeExperience(starButton.dataset.starUrl, 'POST');
                starButton.classList.toggle('is-starred', result.is_starred);
                starButton.querySelector('[data-star-text]').textContent = result.is_starred ? 'Unstar' : 'Star';
                starButton.querySelector('[data-star-count]').textContent = result.star_count;
            } catch (error) {
                notify('Gagal', error.message, 'error');
            } finally {
                starButton.disabled = false;
            }
        } else if (editButton) {
            openModal(experienceCache.get(editButton.dataset.id));
        } else if (deleteButton) {
            if (!window.confirm('Yakin ingin menghapus experience ini?')) return;
            deleteButton.disabled = true;
            try {
                await writeExperience(EXPERIENCE_DETAIL_TEMPLATE.replace(ID_PLACEHOLDER, deleteButton.dataset.id), 'DELETE');
                notify('Berhasil', 'Experience berhasil dihapus.', 'success');
                fetchExperiences();
            } catch (error) {
                notify('Gagal menghapus experience', error.message, 'error');
                deleteButton.disabled = false;
            }
        }
    });

    // Modal dipakai untuk tambah (experience kosong) dan edit (experience terisi).
    function openModal(experience) {
        if (!experienceForm || !modal) return;
        editingId = experience ? experience.id : null;
        experienceForm.reset();

        if (experience) {
            // Ambil jam dari string ISO apa adanya (zona Django), bukan lewat Date browser.
            experienceForm.elements.title.value = experience.title;
            experienceForm.elements.description.value = experience.description;
            experienceForm.elements.category.value = experience.category;
            experienceForm.elements.thumbnail.value = experience.thumbnail || '';
            experienceForm.elements.started_at.value = experience.started_at.slice(0, 16);
            experienceForm.elements.ended_at.value = experience.ended_at ? experience.ended_at.slice(0, 16) : '';
        }

        document.getElementById('add-experience-modal-title').textContent =
            experience ? 'Edit Experience' : 'Tambah Experience Baru';
        document.getElementById('experience-submit').textContent =
            experience ? 'Simpan Perubahan' : 'Tambah Experience';
        modal.showPopover();
    }

    if (addButton) addButton.addEventListener('click', () => openModal(null));

    async function submitExperience(event) {
        event.preventDefault();
        const submitButton = document.getElementById('experience-submit');
        submitButton.disabled = true;

        try {
            const fields = new FormData(experienceForm);
            const payload = {
                title: fields.get('title'),
                description: fields.get('description'),
                category: fields.get('category'),
                thumbnail: fields.get('thumbnail'),
                started_at: fields.get('started_at'),
                ended_at: fields.get('ended_at') || null, // kosong = masih berlangsung
            };

            if (editingId) {
                await writeExperience(EXPERIENCE_DETAIL_TEMPLATE.replace(ID_PLACEHOLDER, editingId), 'PATCH', payload);
            } else {
                await writeExperience(EXPERIENCES_ENDPOINT, 'POST', payload);
            }

            const message = editingId ? 'Experience berhasil diperbarui!' : 'Experience baru berhasil ditambahkan!';
            experienceForm.reset();
            modal.hidePopover();
            notify('Berhasil', message, 'success');
            fetchExperiences();
        } catch (error) {
            notify('Gagal menyimpan experience', error.message, 'error');
        } finally {
            submitButton.disabled = false;
        }
    }

    if (experienceForm) experienceForm.addEventListener('submit', submitExperience);

    // Debounce: request dikirim setelah user berhenti mengetik.
    searchInput.addEventListener('input', function () {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(fetchExperiences, SEARCH_DEBOUNCE_DELAY);
    });

    categoryFilter.addEventListener('change', fetchExperiences);
    sortSelect.addEventListener('change', fetchExperiences);

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        fetchExperiences();
    });

    fetchExperiences();
})();
