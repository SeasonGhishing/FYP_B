// function editPerson(id) {
//     // Retrieve the role associated with the given ID
//     const roleElement = document.querySelector(`[data-id='${id}']`);
//     if (roleElement) {
//         const role = roleElement.dataset.role;
        
//         console.log('Role Element:', roleElement);
//         const rolePlural = role === 'student' ? 'student_register_page' : 'teacher_register_page'; // Adjust for pluralization

//         // Redirect to the appropriate page based on the role
//         window.location.href = `/api/accounts/${rolePlural}/?id=${id}`;
//     } else {
//         console.error('No element found with the specified ID:', id);
//         alert('Error: Invalid ID. Please try again.');
//     }
// }

// function confirmDelete(id) {
//     if (confirm("Are you sure you want to remove this perso?")) {
//         deletePerson(id);
//     }
// }

// function deletePerson(id) {
//     const role = document.querySelector(`[data-id='${id}']`).dataset.role;
//     const rolePlural = role === 'student' ? 'students' : 'teachers'; // Adjust for pluralization

//     fetch(`{{ BASE_URL }}/api/accounts/${rolePlural}/${id}`, {
//         method: 'DELETE',
//     })
//     .then(response => {
//         if (response.ok) {
//             document.querySelector(`[data-id='${id}']`).remove();
//             showToast('User removed successfully', 'success');
//         } else {
//             throw new Error('Failed to delete person');
//         }
//     })
//     .catch(error => {
//         console.error(error);
//         showToast('Something went wrong', 'error');
//     });
// }

// function showToast(message, type) {
//     const toast = document.createElement('div');
//     toast.textContent = message;
//     toast.classList.add('toast');
//     if (type === 'success') {
//         toast.classList.add('success');
//     } else if (type === 'error') {
//         toast.classList.add('error');
//     }
//     document.body.appendChild(toast);

//     setTimeout(() => {
//         toast.classList.add('show');
//     }, 100); // Add a small delay before showing to allow for CSS transition

//     setTimeout(() => {
//         toast.classList.remove('show');
//         setTimeout(() => {
//             toast.remove();
//         }, 500); // Transition duration + delay before removing
//     }, 3000); // Adjust duration as needed

// }

// function attachEventListeners() {
//     const mainPanel = document.querySelector('.main-panel');

//     // Delegate event handling to the main panel
//     mainPanel.addEventListener('click', function(event) {
//         const target = event.target;

//         if (target.classList.contains('edit-button')) {
//             const id = target.closest('.person-row').dataset.id;
//             editPerson(id);
//         } else if (target.classList.contains('delete-button')) {
//             const id = target.closest('.person-row').dataset.id;
//             confirmDelete(id);
//         }
//         // Add more event handling as needed for other buttons or elements
//     });
// }

// function initializeFilters() {
//     const searchInput = document.getElementById('search-input');
//     const rows = document.querySelectorAll('.person-row');
//     const roleFilter = document.getElementById('role-filter');
//     const classFilter = document.getElementById('class-filter');

//     function filterRows() {
//         const selectedRole = roleFilter.value.toLowerCase();
//         const selectedClass = classFilter.value;
//         const searchTerm = searchInput.value.trim().toLowerCase();

//         rows.forEach(function(row) {
//             const personRole = row.dataset.role.toLowerCase();
//             const personClass = row.dataset.class;

//             if ((selectedRole === 'all' || personRole === selectedRole) && (selectedClass === '' || personClass === selectedClass)) {
//                 const name = row.querySelector('.profile-name').textContent.trim().toLowerCase();

//                 if (name.includes(searchTerm)) {
//                     row.style.display = 'table-row';
//                 } else {
//                     row.style.display = 'none';
//                 }
//             } else {
//                 row.style.display = 'none';
//             }
//         });
//     }

//     searchInput.addEventListener('keyup', filterRows);
//     roleFilter.addEventListener('change', filterRows);
//     classFilter.addEventListener('change', filterRows);
// }

// // Remaining functions (editPerson, confirmDelete, deletePerson) remain the same

