document.addEventListener('DOMContentLoaded', function() {
    // Динамическое добавление вопросов
    const addQuestionBtn = document.getElementById('add-question');
    const questionContainer = document.getElementById('questions-container');
    
    if (addQuestionBtn) {
        addQuestionBtn.addEventListener('click', function() {
            const questionType = document.getElementById('question-type').value;
            const questionTemplate = document.getElementById(`${questionType}-template`);
            const newQuestion = questionTemplate.content.cloneNode(true);
            questionContainer.appendChild(newQuestion);
        });
    }

    // Drag and drop для переупорядочивания вопросов
    const sortable = new Sortable(questionContainer, {
        animation: 150,
        handle: '.drag-handle',
        onEnd: function(evt) {
            updateQuestionOrder();
        }
    });
});

function updateQuestionOrder() {
    const questions = document.querySelectorAll('.question-item');
    questions.forEach((question, index) => {
        question.querySelector('input[name*="order"]').value = index;
    });
}