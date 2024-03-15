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