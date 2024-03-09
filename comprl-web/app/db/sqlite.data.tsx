import Database from 'better-sqlite3';
import User from './types';

console.log('Creating users.db');
const db = new Database('users.db', { verbose: console.log });
db.prepare(`
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        token TEXT,
        mu FLOAT NOT NULL DEFAULT 25.0,
        sigma FLOAT NOT NULL DEFAULT 8.333)
    `).run();
db.close();

export async function addUser(username: string, password: string, role: string = 'user') {
    const db = new Database('users.db', { verbose: console.log });
    const stmt = db.prepare('INSERT INTO users(username, password, role) VALUES (?, ?, ?)');
    stmt.run(username, password, role);
    db.close();
}

export async function getUser(username: string, password: string) {
    const db = new Database('users.db', { verbose: console.log });
    const stmt = db.prepare('SELECT * FROM users WHERE username = ?');
    const res = stmt.get(username);
    db.close();
    if (!res) { return undefined }
    if (res.password != password) { return undefined }
    return { id: res.user_id, name: res.username, role: res.role } as User;
}

export async function getAllUsers() {
    const db = new Database('users.db', { verbose: console.log });
    const query = 'SELECT * FROM users';
    const users = db.prepare(query).all();
    db.close();
    return users;
}

export async function getRankedUsers() {
    const users = await getAllUsers();

    const rankedUsers = users.sort((a, b) => {
        // Sort by descending mu (largest first)
        if (b.mu !== a.mu) {
            return b.mu - a.mu;
        }
        // If mu is equal, sort by ascending sigma (smallest first)
        return a.sigma - b.sigma;
    });

    return rankedUsers;
}
