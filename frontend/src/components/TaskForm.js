import React, { useState } from 'react';
import axios from 'axios';

const TaskForm = ({ refreshTasks }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('pending');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title) {
      alert('Title is required');
      return;
    }
    axios.post('/tasks', { title, description, status })
      .then(response => {
        setTitle('');
        setDescription('');
        setStatus('pending');
        refreshTasks();
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>
      <button type="submit">Add Task</button>
    </form>
  );
};

export default TaskForm;
