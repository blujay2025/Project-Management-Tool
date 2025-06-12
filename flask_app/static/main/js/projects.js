// Redirects to appropriate board creation template or existing board template based on new_project button or
// existing_project button click
const board_creation = function board_creation() {
  window.location.href = '/board-creation';
}

const existing_boards = function existing_boards() {
  window.location.href = '/existing-boards';
}

const new_project_button = document.getElementById('new-project');
new_project_button.addEventListener('click', board_creation);

const existing_project_button = document.getElementById('existing-project');
existing_project_button.addEventListener('click', existing_boards);