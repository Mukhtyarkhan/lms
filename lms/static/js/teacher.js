
document.addEventListener('DOMContentLoaded', function () {
    const addCourseBtn = document.getElementById('add-course');
    const formContainer = document.getElementById('form-container');
    const form = document.getElementById('course-form');
    const createCourseUrl = form.dataset.url;

    addCourseBtn.onclick = () => {
        formContainer.style.display = 'block';
        addCourseBtn.style.display = 'none'
    };

    form.onsubmit = function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = fetch(createCourseUrl, {
            method: 'POST',
            headers: {

                'X-CSRFToken': csrftoken
            },
            body: formData
        });


        formContainer.style.display = 'none';
        addCourseBtn.style.display = 'block'
        // form.reset();
    }

    // const viewLessons = document.getElementById('view-lesson');
    // const lessonCard = document.getElementById('lesson');
    // viewLessons.onclick = () => {
    //     viewLessons.style.display = 'none'

    //     lessonCard.style.display = 'block';

    // }


    const viewLessonButtons = document.querySelectorAll('.view-lesson-btn');

    viewLessonButtons.forEach(button => {
        button.addEventListener('click', function () {

            const courseId = button.id.split('-').pop();
            button.style.display = 'none';
            const lessonCard = document.getElementById(`lesson-${courseId}`);
            if (lessonCard) {
                lessonCard.style.display = 'block';
            }
        });
    });





    const deleteCourseButtons = document.querySelectorAll('.delete-course-btn');

    deleteCourseButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const courseId = button.getAttribute('id');

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/teacher/delete-course/${courseId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const courseCard = button.closest('.course-card');
                        if (courseCard) {
                            courseCard.remove();
                        }
                    }
                })
        });
    });





})