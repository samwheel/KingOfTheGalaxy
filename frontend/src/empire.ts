export type Empire = {
    "name": string;
    "color": string;
    "planets": string[];
    "production": {
        "population": number;
        "GDP": number;
        "research": number;
        "defense": number;
    }
}