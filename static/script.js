function loadTopicContent(topicId) {
    fetch(`/get-topic-content/${topicId}/`)
        .then(response => {
            if (!response.ok) {
                console.error('Ошибка запроса:', response.status, response.statusText);
                return;
            }
            return response.text();
        })
        .then(text => {
            try {
                const data = JSON.parse(text);
                const contentDisplay = document.getElementById('content-display');
                contentDisplay.textContent = data.content;
            } catch (error) {
                console.error('Ошибка обработки JSON:', error);
                console.log('Ответ сервера:', text);
            }
        })
        .catch(error => console.error('Error loading content:', error));
}
