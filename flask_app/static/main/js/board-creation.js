// Handles adding of more members to a particular project
let memberId = 2
const additional_members = function additionalMembers() {
    var boardCreationForm = document.getElementById('board-creation-form');
    var submitButton = document.getElementById('board-creation-submit');
    var memberIdInput = document.getElementById('memberIdInput');

    var newInput = document.createElement('input');
    newInput.className = 'board-creation-field';
    newInput.type = 'text';
    newInput.name = 'member' + memberId.toString();
    newInput.placeholder = "Enter member's email";
    newInput.title = "Enter member's email";
    
    boardCreationForm.insertBefore(newInput, submitButton);
    memberIdInput.value = memberId.toString();

    memberId = memberId + 1
}



const more_members_button = document.getElementById('more-members');
more_members_button.addEventListener('click', additional_members);