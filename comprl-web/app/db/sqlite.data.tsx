import Database from 'better-sqlite3';
import User from './types';
import { config } from "config";

console.log(`Creating ${config.user_db_path}`);
const db = new Database(config.user_db_path, { verbose: console.log });
db.prepare(`
        CREATE TABLE IF NOT EXISTS ${config.user_db_name}(
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
    const db = new Database(config.user_db_path, { verbose: console.log });
    const stmt = db.prepare(`INSERT INTO ${config.user_db_name}(username, password, role) VALUES (?, ?, ?)`);
    stmt.run(username, password, role);
    db.close();
}

export async function getUser(username: string, password: string) {
    const db = new Database(config.user_db_path, { verbose: console.log });
    const stmt = db.prepare(`SELECT * FROM ${config.user_db_name} WHERE username = ?`);
    const res = stmt.get(username);
    db.close();
    if (!res) { return undefined }
    if (res.password != password) { return undefined }
    return { id: res.user_id, name: res.username, role: res.role } as User;
}