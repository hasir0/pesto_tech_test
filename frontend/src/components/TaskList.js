import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    refreshTasks();
  }, []);

  const refreshTasks = () => {
    axios.get('/tasks').then(response => setTasks(response.data));
  };

  const updateTask = (id, updatedTask) => {
    axios.put(`/tasks/${id}`, updatedTask)
      .then(response => {
        setTasks(tasks.map(task => (task.id === id ? updatedTask : task)));
      });
  };

  const deleteTask = (id) => {
    axios.delete(`/tasks/${id}`)
      .then(response => {
        setTasks(tasks.filter(task => task.id !== id));
      });
  };

  const filteredTasks = tasks.filter(task => statusFilter === 'all' || task.status === statusFilter);

  return (
    <div>
      <select onChange={(e) => setStatusFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>
      {filteredTasks.map(task => (
        <div key={task.id}>
          <h3>{task.title}</h3>
          <p>{task.description}</p>
          <p>{task.status}</p>
          <button onClick={() => updateTask(task.id, { ...task, status: 'completed' })}>Complete</button>
          <button onClick={() => deleteTask(task.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
