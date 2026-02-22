import React, { useState, useEffect } from 'react';
import { todoService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const TodoDashboard = () => {
    const [todos, setTodos] = useState([]);
    const [newTodoTitle, setNewTodoTitle] = useState('');
    const [newTodoDesc, setNewTodoDesc] = useState('');
    const [editingTodo, setEditingTodo] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { logout } = useAuth();

    const fetchTodos = async () => {
        setLoading(true);
        try {
            const response = await todoService.getAll();
            if (response.data.status) {
                setTodos(response.data.data);
            }
        } catch (err) {
            setError('Failed to fetch todos');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTodos();
    }, []);

    const handleCreateTodo = async (e) => {
        e.preventDefault();
        try {
            const response = await todoService.create(newTodoTitle, newTodoDesc);
            if (response.data.status) {
                setTodos([...todos, response.data.data]);
                setNewTodoTitle('');
                setNewTodoDesc('');
            }
        } catch (err) {
            setError('Failed to create todo');
        }
    };

    const handleDeleteTodo = async (id) => {
        try {
            const response = await todoService.delete(id);
            if (response.data.status) {
                setTodos(todos.filter((t) => t._id !== id));
            }
        } catch (err) {
            setError('Failed to delete todo');
        }
    };

    const handleEditTodo = (todo) => {
        setEditingTodo({ ...todo });
    };

    const handleUpdateTodo = async (e) => {
        e.preventDefault();
        try {
            const response = await todoService.update(editingTodo._id, editingTodo.title, editingTodo.description);
            if (response.data.status) {
                setTodos(todos.map((t) => (t._id === editingTodo._id ? response.data.data : t)));
                setEditingTodo(null);
            }
        } catch (err) {
            setError('Failed to update todo');
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>My Todos</h1>
                <button onClick={logout} className="logout-btn">Logout</button>
            </header>

            {error && <p className="error-message">{error}</p>}

            <section className="todo-form">
                <h2>{editingTodo ? 'Edit Todo' : 'Add New Todo'}</h2>
                <form onSubmit={editingTodo ? handleUpdateTodo : handleCreateTodo}>
                    <input
                        type="text"
                        placeholder="Title"
                        value={editingTodo ? editingTodo.title : newTodoTitle}
                        onChange={(e) => editingTodo
                            ? setEditingTodo({ ...editingTodo, title: e.target.value })
                            : setNewTodoTitle(e.target.value)}
                        required
                    />
                    <textarea
                        placeholder="Description"
                        value={editingTodo ? editingTodo.description : newTodoDesc}
                        onChange={(e) => editingTodo
                            ? setEditingTodo({ ...editingTodo, description: e.target.value })
                            : setNewTodoDesc(e.target.value)}
                        required
                    />
                    <div className="form-actions">
                        <button type="submit">{editingTodo ? 'Update' : 'Add'}</button>
                        {editingTodo && <button type="button" onClick={() => setEditingTodo(null)}>Cancel</button>}
                    </div>
                </form>
            </section>

            <section className="todo-list">
                {loading ? (
                    <p>Loading todos...</p>
                ) : todos.length === 0 ? (
                    <p>No todos found. Add one above!</p>
                ) : (
                    <ul>
                        {todos.map((todo) => (
                            <li key={todo._id} className="todo-item">
                                <div className="todo-content">
                                    <h3>{todo.title}</h3>
                                    <p>{todo.description}</p>
                                </div>
                                <div className="todo-actions">
                                    <button onClick={() => handleEditTodo(todo)}>Edit</button>
                                    <button onClick={() => handleDeleteTodo(todo._id)} className="delete-btn">Delete</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    );
};

export default TodoDashboard;
