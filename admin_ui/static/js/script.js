base_url = 'http://192.168.90.8:8000';

document.addEventListener("DOMContentLoaded", function () {
  selectItem('dashboard');
});

function selectItem(itemName) {
  var items = document.querySelectorAll('.nav-item');
  items.forEach(item => {
    item.classList.remove('selected');
  });

  var selectedItem = document.querySelector('.nav-item[data-item="' + itemName + '"]');
  selectedItem.classList.add('selected');

  loadContent(itemName);
}

// function loadContent(itemName) {
//   var contentPanel = document.querySelector('.main-content');
//   var contentUrl = `/admin_ui/${itemName}/`;  // Adjust the URL based on your Django app structure

//   fetch(contentUrl)
//       .then(response => response.text())
//       .then(data => {
//           contentPanel.innerHTML = data;
//           // After loading the content, attach event listeners and initialize filters
//           // attachEventListeners();
//           initializeFilters();
//       })
//       .catch(error => {
//           console.error('Error fetching content:', error);
//       });
// }

function loadContent(itemName) {
  var contentPanel = document.querySelector('.main-content');
  var contentUrl = `/admin_ui/${itemName}/`;  // Adjust the URL based on your Django app structure

  fetch(contentUrl)
    .then(response => response.text())
    .then(data => {
      contentPanel.innerHTML = data;
      // After loading the content, attach event listeners and initialize filters
      if (itemName === 'people') {
        initializePeopleFilters();
      } else if (itemName === 'routine_table') {
        initializeRoutineFilters();
      }
      else if (itemName === 'attendance') {
        initializeAttendanceFilters();
      }
    })
    .catch(error => {
      console.error('Error fetching content:', error);
    });
}



function editPerson(id) {
  const roleElement = document.querySelector(`.main-content [data-id='${id}']`);
  if (roleElement) {
    const role = roleElement.dataset.role;
    const rolePlural = role === 'student' ? 'student' : 'teacher';

    // Load content for the selected item
    // Redirect to the appropriate page based on the role after content is loaded
    window.location.href = `/admin_ui/${rolePlural}/?id=${id}`;
  } else {
    console.error('No element found with the specified ID:', id);
    alert('Error: Invalid ID. Please try again.');
  }
}



function confirmDelete(id) {
  if (confirm("Are you sure you want to remove this person?")) {
    deletePerson(id);
  }
}

function deletePerson(id) {
  const role = document.querySelector(`.main-content [data-id='${id}']`).dataset.role;
  const rolePlural = role === 'student' ? 'students' : 'teachers'; // Adjust for pluralization
  // change url

  fetch(`${base_url}/api/accounts/${rolePlural}/${id}`, {
    method: 'DELETE',
  })
    .then(response => {
      if (response.ok) {
        document.querySelector(`.main-content [data-id='${id}']`).remove();
        showToast('User removed successfully', 'success');
      } else {
        throw new Error('Failed to delete person');
      }
    })
    .catch(error => {
      console.error(error);
      showToast('Something went wrong', 'error');
    });
}

function initializePeopleFilters() {
  const searchInput = document.getElementById('search-input');
  const rows = document.querySelectorAll('.person-row');
  const roleFilter = document.getElementById('role-filter');
  const classFilter = document.getElementById('class-filter');

  function filterRows() {
    const selectedRole = roleFilter.value.toLowerCase();
    const selectedClass = classFilter.value;
    const searchTerm = searchInput.value.trim().toLowerCase();

    rows.forEach(function (row) {
      const personRole = row.dataset.role.toLowerCase();
      const personClass = row.dataset.class;

      if ((selectedRole === 'all' || personRole === selectedRole) &&
        (selectedClass === '' || personClass === selectedClass)) {
        const name = row.querySelector('.profile-name').textContent.trim().toLowerCase();

        if (name.includes(searchTerm)) {
          row.style.display = 'table-row';
        } else {
          row.style.display = 'none';
        }
      } else {
        row.style.display = 'none';
      }
    });
  }

  searchInput.addEventListener('keyup', filterRows);
  roleFilter.addEventListener('change', filterRows);
  classFilter.addEventListener('change', filterRows);
}

function initializeRoutineFilters() {
  const searchInput = document.getElementById('routine-search-input');
  const rows = document.querySelectorAll('.routine-row');
  const classFilter = document.getElementById('routine-class-filter');

  function filterRows() {
    const selectedClass = classFilter.value;
    const searchTerm = searchInput.value.trim().toLowerCase();

    rows.forEach(function (row) {
      const routineClass = row.dataset.class;
      const subject = row.cells[1].textContent.trim().toLowerCase();
      const assignedTeacher = row.cells[3].textContent.trim().toLowerCase();

      if ((selectedClass === '' || routineClass === selectedClass) &&
        (subject.includes(searchTerm) || assignedTeacher.includes(searchTerm))) {
        row.style.display = 'table-row';
      } else {
        row.style.display = 'none';
      }
    });
  }

  searchInput.addEventListener('keyup', filterRows);
  classFilter.addEventListener('change', filterRows);
}

function initializeAttendanceFilters() {
  const searchInput = document.getElementById('search-input');
  // const rows = document.querySelectorAll('.person-row');
  const roleFilter = document.getElementById('role-filter');
  const monthFilter = document.getElementById('month-filter');
  const attendanceTableBody = document.getElementById('attendance-table-body');
  const classFilter = document.getElementById('class-filter');
  const rows = attendanceTableBody.getElementsByClassName('person-row');

  function filterTable() {
    const searchText = searchInput.value.toLowerCase();
    const selectedClass = classFilter.value;
    const selectedRole = roleFilter.value;
    const selectedMonth = monthFilter.value;

    for (const row of rows) {
      const name = row.children[1].textContent.toLowerCase();
      const role = row.getAttribute('data-role');
      const classId = row.getAttribute('data-class');
      const date = row.getAttribute('data-date');
      const month = date.split('-')[1];

      const matchesSearch = name.includes(searchText);
      const matchesRole = selectedRole === 'all' || role === selectedRole;
      const matchesClass = selectedClass === '' || classId === selectedClass;
      const matchesMonth = selectedMonth === '' || month === selectedMonth;

      if (matchesSearch && matchesRole && matchesClass && matchesMonth) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    }
  }

  searchInput.addEventListener('input', filterTable);
  roleFilter.addEventListener('change', filterTable);
  classFilter.addEventListener('change', filterTable);
  monthFilter.addEventListener('change', filterTable);
}

function showToast(message, type) {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.classList.add('toast');
  if (type === 'success') {
    toast.classList.add('success');
  } else if (type === 'error') {
    toast.classList.add('error');
  }
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('show');
  }, 100);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      toast.remove();
    }, 500); // Transition duration + delay before removing
  }, 3000); // Adjust duration as needed
}

// script.js

function previewImage(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function () {
    const image = document.createElement('img');
    image.src = reader.result;
    image.style.width = '97px';
    image.style.height = '97px';
    image.style.borderRadius = '50%'; // Set border radius to match circle
    image.style.objectFit = 'cover';
    document.querySelector('.main-content .circle').innerHTML = '';
    document.querySelector('.main-content .circle').appendChild(image);
  }

  reader.readAsDataURL(file);
}



// routine section


function editRoutine(id) {
  window.location.href = `/admin_ui/routine_form/?id=${id}`;
}

function confirmDeleteRoutine(id) {
  if (confirm("Are you sure you want to remove this routine?")) {
    deleteRou(id);
    setTimeout(() => {
      window.location.href = `${base_url}/admin_ui/base/`;

    }, 3000);
  }
}

function deleteRou(id) {
  // Ensure base_url is correctly set or imported from elsewhere in your script

  fetch(`${base_url}/api/routine/${id}`, {
    method: 'DELETE',
  })
    .then(response => {
      if (response.ok) {
        const announcementElement = document.querySelector(`.main-content [data-id='${id}']`);
        if (announcementElement) {
          announcementElement.remove();
          showToast('Routine removed successfully', 'success');
        } else {
          showToast('Routine removed successfully', 'success');
        }
      } else {
        throw new Error('Failed to delete routine');
      }
    })
    .catch(error => {
      console.error(error);
      showToast('Something went wrong', 'error');
    });
}

function goBack() {
  window.history.back();
}

function approveLeaveRequest(leaveRequestId) {
  sendRequest(leaveRequestId, 'approve');
}

function rejectLeaveRequest(leaveRequestId) {
  sendRequest(leaveRequestId, 'reject');
}

function sendRequest(leaveRequestId, action) {
  // change url
  fetch(`${base_url}/api/attendance/informed/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is included in the request headers
    },
    body: JSON.stringify({
      leave_request_id: leaveRequestId,
      action: action
    })
  }).then(response => {
    if (response.ok) {
      alert('Leave request status updated successfully');
      location.reload(); // Reload the page after successful update
    } else {
      alert('Failed to update leave request status');
    }
  }).catch(error => {
    console.error('Error:', error);
    alert('An error occurred while processing the request');
  });
}

// Function to get CSRF token from cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// success for announcement delete.

function deleteAnn(id) {
  // Ensure base_url is correctly set or imported from elsewhere in your script

  fetch(`${base_url}/api/announcements/${id}`, {
    method: 'DELETE',
  })
    .then(response => {
      if (response.ok) {
        const announcementElement = document.querySelector(`.main-content [data-id='${id}']`);
        if (announcementElement) {
          announcementElement.remove();
          showToast('Announcement removed successfully', 'success');
        } else {
          showToast('Announcement removed successfully', 'success');
        }
      } else {
        throw new Error('Failed to delete announcement');
      }
    })
    .catch(error => {
      console.error(error);
      showToast('Something went wrong', 'error');
    });
}

function confirmDeleteAnnouncement(id) {
  if (confirm("Are you sure you want to remove this announcement?", id)) {
    deleteAnn(id);
    setTimeout(() => {
      window.location.href = `${base_url}/admin_ui/base/`;

    }, 3000);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Fetch the attendance percentage from the template context
  const attendancePercentage = JSON.parse(document.getElementById('attendance-percentage-data').textContent);

  // Update the SVG circle
  const meter = document.querySelector('.meter');
  const radius = meter.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;

  // Calculate the stroke-dasharray value based on the percentage
  const dashArray = `${(attendancePercentage / 100) * circumference}, ${circumference}`;
  meter.style.strokeDasharray = dashArray;

  // Update the text with the percentage
  document.getElementById('attendance-percentage').textContent = `${attendancePercentage.toFixed(2)}% Present`;
});
