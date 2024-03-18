import Database from 'better-sqlite3';
import { User, Statistics, Game, GameResult } from './types';
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
    const stmt = userDB.prepare('INSERT INTO users(username, password, role, token) VALUES (?, ?, ?,?)');
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



export async function searchUsers(names: string[]) {
    var users = new Set();
    const db = new Database('users.db', { verbose: console.log });
    names.forEach(( name: string) => {
        const query = '%' + name + '%'
        const stmt = db.prepare('SELECT * FROM users WHERE username LIKE ?');
        const res = stmt.all(query)
        res.forEach(user => users.add(JSON.stringify({ id: user.user_id, name: user.username, role: user.role, token: user.token } as User)));
    })
    db.close()

    var result = Array.from(users).map(JSON.parse)
    const exact_name = result.findIndex((user) => names.includes(user.name))
    if (exact_name == -1) return result

    const swap = result[0]
    result[0] = result[exact_name]
    result[exact_name] = swap
    return result
    
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


export async function composeGame(game: Game, name1: string, name2: string) {
    const username1 = name1 || await getUsername(game.user1)
    const username2 = name2 || await getUsername(game.user2)
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

    if (!game) return null
    return composeGame(game as Game)

}

export async function searchGames(search: string) {
    const keywords = search.split(" ", 3) // search for max 3 keywords
    var results = new Set<GameResult>()

    const result_ids = await Promise.all(keywords.map(getGame))
    result_ids.forEach((game) => {if (game) results.add(JSON.stringify(game))})

    const gameDB = new Database('game.db')
    const users = await searchUsers(keywords)
    await Promise.all(users.map( async user => {
        const stmt = gameDB.prepare('SELECT * FROM data WHERE user1=? OR user2=?')
        const games = stmt.all(user.id, user.id)
        await Promise.all(games.reverse().map(async (game) => {
            const composedGame = game.user1 == user.id ? await composeGame( game, user.name, null) : await composeGame( game, null, user.name)
            results.add(JSON.stringify(composedGame)) 
        }))
    }))

    return { games: Array.from(results).map(JSON.parse) }
}
