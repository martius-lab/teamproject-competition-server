import Database from 'better-sqlite3';
import { User, Statistics, Game } from './types';
import { v4 as uuidv4 } from 'uuid';

console.log('Creating users.db');
const userDB = new Database('users.db', { verbose: console.log });
userDB.prepare(`
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        token TEXT,
        mu FLOAT NOT NULL DEFAULT 25.0,
        sigma FLOAT NOT NULL DEFAULT 8.333)
    `).run();
userDB.close();

console.log('Creating game.db');
const gameDB = new Database('game.db', { verbose: console.log });
gameDB.prepare(`
    CREATE TABLE IF NOT EXISTS data (
    game_id TEXT NOT NULL PRIMARY KEY,
    user1 INTEGER NOT NULL, 
    user2 INTEGER NOT NULL, 
    score1 FLOAT NOT NULL, 
    score2 FLOAT NOT NULL,
    start_time,
    end_state INTEGER NOT NULL,
    winner INTEGER,
    disconnected INTEGER)
    `).run();
gameDB.close();

export async function addUser(username: string, password: string, role: string = 'user') {
    const userDB = new Database('users.db', { verbose: console.log });
    const token = uuidv4();
    const stmt = userDB.prepare('INSERT INTO users(username, password, role, token) VALUES (?, ?, ?, ?)');
    stmt.run(username, password, role, token);
    userDB.close();
}

export async function getUser(username: string, password: string) {
    const userDB = new Database('users.db', { verbose: console.log });
    const stmt = userDB.prepare('SELECT * FROM users WHERE username = ?');
    const res = stmt.get(username);
    userDB.close();
    if (!res) { return undefined }
    if (res.password != password) { return undefined }
    return { id: res.user_id, name: res.username, role: res.role, token: res.token } as User;
}

export async function getUsername(user_id: number) {
    const userDB = new Database('users.db', { verbose: console.log });
    const stmt = userDB.prepare('SELECT username FROM users WHERE user_id = ?');
    const res = stmt.get(user_id);
    userDB.close();
    return res.username;
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
        // Sort by descending (mu - sigma)
        return (b.mu - b.sigma) - (a.mu - a.sigma);
    });

    return rankedUsers;
}



export async function getStatistics(user_id: number) {
    const gameDB = new Database('game.db', { verbose: console.log });

    const stmt_played = gameDB.prepare('SELECT COUNT(*) FROM data WHERE user1 = ? OR user2 = ?');
    const playedGames = stmt_played.get(user_id, user_id)['COUNT(*)'];

    const stmt_won = gameDB.prepare('SELECT COUNT(winner) FROM data WHERE winner = ?');
    const wonGames = stmt_won.get(user_id)['COUNT(winner)'];

    const stmt_disconnect = gameDB.prepare('SELECT COUNT(disconnected) FROM data WHERE disconnected = ?');
    const disconnectedGames = stmt_disconnect.get(user_id)['COUNT(disconnected)'];

    gameDB.close();

    return { playedGames: playedGames, wonGames: wonGames, disconnectedGames: disconnectedGames } as Statistics
}


export async function composeGame(game: Game) {
    const username1 = await getUsername(game.user1)
    const username2 = await getUsername(game.user2)
    if (!username1 || !username2) { return null }
    return {
        game_id: game.game_id,
        participants: [
            {
                name: username1,
                score: game.score1,
                winner: (game.user1 == game.winner),
                disconnected: (game.user1 == game.disconnected)
            },
            {
                name: username2,
                score: game.score2,
                winner: (game.user2 == game.winner),
                disconnected: (game.user2 == game.disconnected)
            }
        ],
        start_time: game.start_time,
        end_state: game.end_state,
    }
}

export async function getGame(game_id: string) {
    const gameDB = new Database('game.db', { verbose: console.log });
    const stmt = gameDB.prepare('SELECT * FROM data WHERE game_id=?');
    const game = stmt.get(game_id)
    gameDB.close();

    if (!game) { return null }
    return composeGame(game as Game)

}

export async function editUser(user_id: number, username: string, password: string, role: string, token: string, mu: number, sigma: number) {
    // edits the user with the given user_id
    const userDB = new Database('users.db', { verbose: console.log });
    const stmt = userDB.prepare('UPDATE users SET username = ?, password = ?, role = ?, token = ?, mu = ?, sigma = ? WHERE user_id = ?');
    stmt.run(username, password, role, token, mu, sigma, user_id);
    userDB.close();
}

export async function searchGames(search: string) {
    return {
        games: [
            {
                game_id: 'adasdas-adasd-asdasd-asdasd-asdasd',
                participants: [{ name: 'HelloWorldHelloWorld', score: 10, winner: true, disconnected: false }, { name: 'HelloWorld', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '5678',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '91011',
                participants: [{ name: 'user1', score: 10, winner: false, disconnected: true }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '121314',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 1,
            },
            {
                game_id: '151617',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 2,
            },
            {
                game_id: '181920',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 2,
            },
            {
                game_id: '212223',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '242526',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '272829',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '303132',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '333435',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '363738',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '394041',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '424344',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '454647',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '484950',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '515253',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '545556',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            },
            {
                game_id: '575859',
                participants: [{ name: 'user1', score: 10, winner: true, disconnected: false }, { name: 'user2', score: 5, winner: false, disconnected: false }],
                start_time: '2021-10-10 10:00:00',
                end_state: 0,
            }
        ]
    }
}
