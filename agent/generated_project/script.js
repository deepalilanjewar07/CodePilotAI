// Get UI components (matching your HTML)
const form = document.getElementById('create-task-form');
const todoList = document.getElementById('todo-list');
const todoInput = document.getElementById('task-input');

// Store tasks
let todoItems = [];

// Add new task
function addTodoItem() {
  const todoText = todoInput.value;

  if (todoText.trim() === '') {
    displayNotification("Please enter a task", "error");
    return;
  }

  todoItems.push({text:todoText});
  renderTodoList();
  todoInput.value = '';

  displayNotification("Task added successfully!", "success");
}

// Delete task
function deleteTodoItem(index) {
  todoItems.splice(index, 1);
  renderTodoList();
}

// Render list
function renderTodoList() {
  todoList.innerHTML = '';

  todoItems.forEach((item, index) => {
    const li = document.createElement('li');
    li.classList.add('task-item');

    li.innerHTML = `
      <span>${item.text}</span>
      <button class="delete-btn">Delete</button>
    `;

    // delete button
    li.querySelector('.delete-btn').addEventListener('click', () => {
      deleteTodoItem(index);
    });

    todoList.appendChild(li);
  });
}

// Form submit
form.addEventListener('submit', function (e) {
  e.preventDefault(); // 🔥 stop page reload

  const taskText = todoInput.value.trim();

  if (taskText === '') return;

  addTodoItem(taskText);

  todoInput.value = '';
});

function displayNotification(message, type = "success") {
  const container = document.getElementById("notifications-container");

  const note = document.createElement("div");
  note.textContent = message;
  note.style.padding = "10px";
  note.style.marginTop = "5px";
  note.style.borderRadius = "5px";
  note.style.color = "#333";

  if (type === "error") {
    note.style.backgroundColor = "#ffdddd";
  } else {
    note.style.backgroundColor = "#ddffdd";
  }

  container.appendChild(note);

  setTimeout(() => {
    note.remove();
  }, 3000);
}