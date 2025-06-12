// Adds a new card whenever any of the add buttons on any of the lists is clicked
const addCard = function addCard(listId) {
  const list = document.getElementById(listId);
  
  const card = document.createElement("div");
  card.className = "card";
  card.setAttribute("draggable", "true");
  card.addEventListener("dragstart", dragStart);

  const textarea = document.createElement("textarea");
  textarea.value = "Type your task details...";
  textarea.className = "card-text-area";
  textarea.rows = 5;
  textarea.cols = 20;
  textarea.disabled = true;
  card.appendChild(textarea);
  
  card_dict = {'project_name': list.parentElement.getAttribute("data-board"), 'status': listId, 'card_content': textarea.value, 'request_type': "INSERT"}
  jQuery.ajax({
    url: "/cardstableupdate",
    data: card_dict,
    type: "POST",
    success:function(returned_data){
          returned_data = JSON.parse(returned_data);
          if (returned_data.success == 1) {
            card.id = returned_data.card_id.toString()

            const editButton = document.createElement("button");
            editButton.textContent = "Edit Card";
            if (listId == 'todo') {
              editButton.id = "edit-button-todo-" + returned_data.card_id.toString()
            } else if (listId == 'doing'){
              editButton.id = "edit-button-doing-" + returned_data.card_id.toString()
            } else {
              editButton.id = "edit-button-completed-" + returned_data.card_id.toString()
            }
            editButton.onclick = function() { editCard(this); };
            editButton.className = "edit-button"
            card.appendChild(editButton);

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete Card";
            if (listId == 'todo') {
              deleteButton.id = "delete-button-todo-" + returned_data.card_id.toString()
            } else if (listId == 'doing'){
              deleteButton.id = "delete-button-doing-" + returned_data.card_id.toString()
            } else {
              deleteButton.id = "delete-button-completed-" + returned_data.card_id.toString()
            }
            deleteButton.onclick = function() { deleteCard(this); };
            deleteButton.className = "delete-button"
            card.appendChild(deleteButton);

            textarea.id = "card-text-area-" + returned_data.card_id.toString()
            
            list.insertBefore(card, list.lastChild.previousSibling);
            
            textarea.addEventListener("keydown", function(event) {
              if (event.key === "Enter") {
                  textarea.disabled = true;
                  var board = textarea.parentElement.parentElement.parentElement;
                  var boardName = board.getAttribute("data-board");
                  var card_content = textarea.value
                  saveCard(card_content, textarea, boardName);
              }
            });
          }
        }
  });
  
}


// Saves a card with new context and also checks to see if a card with the same content is already part of a list, in which case, it deletes the card
const saveCard = function savecard(card_content, textarea, boardName) {
  card_entry_data = {'project_name': boardName, 'status': textarea.parentElement.parentElement.id, 'card_content': card_content}
  jQuery.ajax({
    url: "/card-already-exists",
    data: card_entry_data,
    type: "POST",
    success:function(returned_data){
          returned_data = JSON.parse(returned_data);
          if (returned_data.success == 1) {
            card_dict = {'project_name': boardName, 'status': textarea.parentElement.parentElement.id, 'card_content': card_content, 'request_type': "UPDATE", 'card_id': textarea.parentElement.id}
            jQuery.ajax({
              url: "/cardstableupdate",
              data: card_dict,
              type: "POST"
            });
          } else {
              const card = textarea.parentElement;
              card_dict = {'card_id': card.id}
              jQuery.ajax({
                    url: "/deletecard",
                    data: card_dict,
                    type: "POST"
                });
              card.remove();
          }
        }
  });
}

// Opens the textarea of a card to input in new content
const editCard = function editCard(button) {
  const card = button.parentElement;
  const textarea = card.querySelector("textarea");
  textarea.disabled = false;
  textarea.focus();
  textarea.select();
}

// Deletes the card and also deletes the associated card information from the cards table
const deleteCard = function deleteCard(button) {
  const card = button.parentElement;
  card_dict = {'card_id': card.id}
  jQuery.ajax({
        url: "/deletecard",
        data: card_dict,
        type: "POST"
    });
  card.remove();
}

// Text area update function for cards that re-render when you open up a board brand new
const textAreaUpdate = function textAreaUpdate(event) {
  if (event.key === "Enter") {
        var textarea = event.target;
        textarea.disabled = true;
        var board = textarea.parentElement.parentElement.parentElement;
        var boardName = board.getAttribute("data-board");
        var card_content = textarea.value
        saveCard(card_content, textarea, boardName);
  }
}

// Handles the drag and drop logic for the cards
const allowDrop = function allowDrop(event) {
    event.preventDefault();  
}

const dragStart = function dragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.id);
}

const dropIt = function dropIt(event) {
    event.preventDefault();  
    let sourceId = event.dataTransfer.getData("text/plain");
    let sourceIdElement = document.getElementById(sourceId);
    let sourceIdParentElement = sourceIdElement.parentElement;
    
    
    let targetElement = event.target;
    let targetParentElement = targetElement.parentElement;

    let between_lists = true;

    if (targetElement.className === sourceIdElement.className) {
        if (targetParentElement.id === sourceIdParentElement.id) {
            between_lists = false;
        }
    } else {
        if (targetElement.id === sourceIdParentElement.id) {
            between_lists = false;
        }
    }

    if (targetElement.id == "to-do-add" || targetElement.id == "doing-add" || targetElement.id == "completed-add" || targetElement.className == "edit-button" || targetElement.className == "delete-button") {
      between_lists = false;
    }

    if (between_lists === true) {
        if (targetElement.className === sourceIdElement.className) {
            old_status = sourceIdParentElement.id
            old_card_id = sourceIdElement.id;

            targetParentElement.insertBefore(sourceIdElement, targetParentElement.lastChild.previousSibling);

            drag_and_drop_dict = {'project_name': targetParentElement.parentElement.getAttribute("data-board"), 'old_card_id': old_card_id, 'new_status': targetParentElement.id}

            jQuery.ajax({
                url: "/draganddropupdate",
                data: drag_and_drop_dict,
                type: "POST"
            });
        } else {
            old_status = sourceIdParentElement.id
            old_card_id = sourceIdElement.id;

            targetElement.insertBefore(sourceIdElement, targetElement.lastChild.previousSibling);

            drag_and_drop_dict = {'project_name': targetElement.parentElement.getAttribute("data-board"), 'old_card_id': old_card_id, 'new_status': targetElement.id}

            jQuery.ajax({
                url: "/draganddropupdate",
                data: drag_and_drop_dict,
                type: "POST"
            });
        }
      }
}


// Adds all the event listeners to associated elements in the board
const to_do_add_button = document.getElementById('to-do-add');
to_do_add_button.addEventListener('click', function(){addCard('todo')});

const doing_add_button = document.getElementById('doing-add');
doing_add_button.addEventListener('click', function(){addCard('doing')});

const completed_add_button = document.getElementById('completed-add');
completed_add_button.addEventListener('click', function(){addCard('completed')});


document.addEventListener('click', function (event) {
  if (event.target.classList.contains('edit-button')) {
    editCard(event.target);
  }
  if (event.target.classList.contains('delete-button')) {
    deleteCard(event.target);
  }
});