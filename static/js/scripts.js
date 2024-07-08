document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('hamburger-menu').addEventListener('click', function() {
        var navLinks = document.getElementById('nav-links');
        if (navLinks.style.display === 'block') {
            navLinks.style.display = 'none';
        } else {
            navLinks.style.display = 'block';
        }
    });

    document.getElementById('semester').addEventListener('change', function() {
        var semester = this.value;
        window.location.href = '/semester/' + semester;
    });
});

function filterCourses() {
    var input, filter, ul, li, i, txtValue, hasMatches = false;
    input = document.getElementById('search-bar');
    filter = input.value.toUpperCase();
    ul = document.getElementById('courses-list');
    li = ul.getElementsByClassName('course-item');

    for (i = 0; i < li.length; i++) {
        txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            hasMatches = true;
        } else {
            li[i].style.display = "none";
        }
    }

    if (!hasMatches) {
        ul.style.display = "none";
    } else {
        ul.style.display = "";
    }
}

function openCourseFilesDialog(semester, course) {
    fetch(`/get_course_files/${semester}/${course}`)
        .then(response => response.json())
        .then(data => {
            var dialogContent = `
                <h1>${course} Files</h1>
                <h3>Semester: ${semester}</h3>
                <ul>
                    ${data.course_files.map(file => `<li><a href="/uploads/${semester}/${course}/${file}" target="_blank">${file}</a></li>`).join('')}
                </ul>
                <a href="/semester/${semester}">Back to Semester</a>
            `;
            document.getElementById('course-files-content').innerHTML = dialogContent;
            document.getElementById('course-files-dialog').showModal();
        })
        .catch(error => {
            console.error('Error fetching course files:', error);
        });
}

function closeCourseFilesDialog() {
    document.getElementById('course-files-dialog').close();
}
