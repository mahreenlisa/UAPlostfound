document.addEventListener('DOMContentLoaded', function () {
    const foundItemSelect = document.querySelector('#id_found_item');

    if (!foundItemSelect) return;

    foundItemSelect.addEventListener('change', function () {
        const foundItemId = this.value;
        if (!foundItemId) return;

        fetch(`/admin/items/claimattempt/get-questions/${foundItemId}/`)
            .then(response => response.json())
            .then(data => {
                const questions = data.questions || [];
                for (let i = 0; i < 3; i++) {
                    const elem = document.querySelector(`#question${i + 1}`);
                    if (elem) {
                        elem.textContent = questions[i] || '-';
                    }
                }
            })
            .catch(error => console.error('Error fetching questions:', error));
    });
});
