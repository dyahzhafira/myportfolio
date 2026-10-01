(function () {
    const loadingState = document.getElementById('experience-loading');
    const errorState = document.getElementById('experience-error');
    const emptyState = document.getElementById('experience-empty');
    const gridContainer = document.getElementById('experience-grid');
    const searchForm = document.getElementById('experience-search-form');
    const searchInput = document.getElementById('experience-search-input');
    const experienceForm = document.getElementById('experience-form');

    if (!gridContainer) return;

    const SEARCH_DEBOUNCE_DELAY = 300;
    let searchDebounceTimer;
    let experiencesAbortController;

    function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showGrid = false }) {
        loadingState.classList.toggle('hide', !showLoading);
        errorState.classList.toggle('hide', !showError);
        emptyState.classList.toggle('hide', !showEmpty);
        gridContainer.classList.toggle('hide', !showGrid);
    }

    function buildExperienceCardElement(item) {
        const experience = item.fields;
        const experienceId = item.id;

        const articleElement = document.createElement('article');
        articleElement.className = 'project-card';

        const starUrl = EXPERIENCE_STAR_URL_TEMPLATE.replace('00000000-0000-0000-0000-000000000000', experienceId);

        const isStarredClass = experience.is_starred ? ' is-starred' : '';
        const starText = experience.is_starred ? 'Unstar' : 'Star';
        const starTitle = experience.star_count > 0
            ? `Dibintangi oleh ${escapeHtml(experience.starred_by_names)}`
            : 'Jadilah yang pertama memberi star';
        const statusText = experience.is_ongoing ? 'Sedang berlangsung' : 'Selesai';

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
            </div>
        `;

        return articleElement;
    }

    async function fetchExperiences(searchQuery = '') {
        if (experiencesAbortController) experiencesAbortController.abort();
        experiencesAbortController = new AbortController();

        try {
            displayPageSection({ showLoading: true });

            const params = new URLSearchParams();
            if (searchQuery) params.set('title', searchQuery);

            const url = params.toString() ? `${EXPERIENCES_DATA_ENDPOINT}?${params.toString()}` : EXPERIENCES_DATA_ENDPOINT;

            const response = await fetch(url, {
                headers: { 'Accept': 'application/json' },
                signal: experiencesAbortController.signal,
            });

            if (!response.ok) throw new Error('Failed to fetch data');

            const experienceData = await response.json();

            if (experienceData.length === 0) {
                displayPageSection({ showEmpty: true });
            } else {
                gridContainer.innerHTML = '';
                experienceData.forEach((item) => {
                    gridContainer.appendChild(buildExperienceCardElement(item));
                });
                displayPageSection({ showGrid: true });
            }
        } catch (error) {
            if (error.name === 'AbortError') return;
            console.error('Error loading experiences:', error);
            displayPageSection({ showError: true });
        }
    }

    // toggle star lewat AJAX
    gridContainer.addEventListener('click', async function (event) {
        const button = event.target.closest('[data-star-button]');
        if (!button) return;

        button.disabled = true;
        try {
            const response = await fetch(button.dataset.starUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });

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

    // search debouncing
    function searchExperiences() {
        fetchExperiences(searchInput.value.trim());
    }

    searchInput.addEventListener('input', function () {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(searchExperiences, SEARCH_DEBOUNCE_DELAY);
    });

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchExperiences();
    });

    // modal tambah experience via AJAX
    function closeExperienceModal() {
        const modal = document.getElementById('add-experience-modal');
        if (modal) modal.hidePopover();
    }

    async function addExperience(event) {
        event.preventDefault();
        const submitButton = experienceForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;

        try {
            const response = await fetch(CREATE_EXPERIENCE_ENDPOINT, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: new FormData(experienceForm),
            });

            const result = await response.json().catch(() => ({}));

            if (response.ok) {
                experienceForm.reset();
                closeExperienceModal();
                if (typeof showToast === 'function') {
                    showToast('Berhasil', 'Experience baru berhasil ditambahkan!', 'success');
                }
                fetchExperiences(searchInput.value.trim());
            } else {
                const errorMessages = result.errors
                    ? Object.values(result.errors).flat().map((error) => error.message)
                    : [result.message || `Terjadi kesalahan (status ${response.status}).`];
                if (typeof showToast === 'function') {
                    showToast('Gagal menambahkan experience', errorMessages.join(' '), 'error');
                }
            }
        } catch (error) {
            console.error('Error adding experience:', error);
            if (typeof showToast === 'function') {
                showToast('Gagal menambahkan experience', 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
            }
        } finally {
            submitButton.disabled = false;
        }
    }

    if (experienceForm) {
        experienceForm.addEventListener('submit', addExperience);
    }

    fetchExperiences(searchInput.value.trim());
})();
