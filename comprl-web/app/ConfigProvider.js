import { readFileSync } from 'fs';
import { parse } from 'toml';
const configFilePath = 'config.toml';
let configData;
try {
    const tomlData = readFileSync(configFilePath, 'utf8');
    const parsedData = parse(tomlData);
    configData = JSON.stringify(parsedData);
} catch (error) {
    console.error('Fehler beim Lesen der Konfigurationsdatei:', error);
    process.exit(1);
}


export const config = configData;