export interface User {
    id: number;
    name: string;
    role: "admin" | "user";
    token: string;
}

export interface Statistics {
    playedGames: number;
    wonGames: number;
    disconnectedGames: number
}

export interface GameResult {
    game_id: string;
    participants: [{name: string, score: number, winner: boolean, disconnected: boolean}]
    start_time: string;
    end_state: number;
}