interface User {
    id: number;
    name: string;
    role: "admin" | "user";
    token: string;
}

export default User