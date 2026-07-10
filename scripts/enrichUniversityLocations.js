const fs = require('fs');
const path = require('path');

const dbDir = path.join(__dirname, '../data_base');

const countryMap = {
    'almanya.json': 'Germany',
    'amerika.json': 'United States',
    'austria.json': 'Austria',
    'belcika.json': 'Belgium',
    'cin.json': 'China',
    'danimarka.json': 'Denmark',
    'fransa.json': 'France',
    'hollanda.json': 'Netherlands',
    'ingiltere.json': 'United Kingdom',
    'ispanya.json': 'Spain',
    'isvec.json': 'Sweden',
    'isvicre.json': 'Switzerland',
    'italy.json': 'Italy',
    'japonya.json': 'Japan',
    'kore.json': 'South Korea',
    'portekiz.json': 'Portugal',
    'rusya.json': 'Russia',
};

async function geocode(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;
    try {
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        });
        if (response.ok) {
            const data = await response.json();
            if (data && data.length > 0) return data[0];
        } else {
            console.error(`HTTP Error ${response.status} for ${query}`);
        }
    } catch (e) {
        console.error(`Fetch Error for ${query}: ${e.message}`);
    }
    return null;
}

function getValue(obj, keys) {
    for (const k of keys) {
        if (obj[k] !== undefined) return obj[k];
    }
    return null;
}

function getString(val) {
    if (!val) return '';
    if (typeof val === 'string') return val;
    if (typeof val === 'object') return val.en || val.tr || '';
    return String(val);
}

async function main() {
    let totalEnriched = 0;
    const files = fs.readdirSync(dbDir);
    
    for (const file of files) {
        if (!file.endsWith('.json') || file === 'taxonomy.json') continue;
        
        const filepath = path.join(dbDir, file);
        let data;
        try {
            data = JSON.parse(fs.readFileSync(filepath, 'utf8'));
        } catch (e) {
            continue;
        }
        
        if (!Array.isArray(data)) continue;
        
        let modified = false;
        const defaultCountry = countryMap[file] || '';
        
        for (const record of data) {
            if (record.location && record.location.latitude) continue;
            
            let city = getString(getValue(record, ['City', 'city']));
            let country = getString(getValue(record, ['Country', 'country'])) || defaultCountry;
            let uniName = getString(getValue(record, ['University_Name', 'name', 'university_name']));
            
            if (!city && !country) continue;
            
            console.log(`Geocoding ${uniName} in ${city}, ${country}...`);
            
            let result = null;
            let confidence = 'exact';
            
            if (uniName) {
                const query = city ? `${uniName}, ${city}, ${country}` : `${uniName}, ${country}`;
                result = await geocode(query);
                await new Promise(r => setTimeout(r, 1100));
            }
            
            if (!result && city) {
                console.log(`Fallback to city level for ${city}, ${country}...`);
                const query = `${city}, ${country}`;
                result = await geocode(query);
                confidence = 'city';
                await new Promise(r => setTimeout(r, 1100));
            }
            
            if (result) {
                record.location = {
                    country: country,
                    city: city,
                    latitude: parseFloat(result.lat),
                    longitude: parseFloat(result.lon),
                    locationConfidence: confidence
                };
                modified = true;
                totalEnriched++;
                console.log(`Found: ${result.lat}, ${result.lon} (${confidence})`);
            } else {
                console.log(`NOT FOUND: ${uniName}`);
            }
        }
        
        if (modified) {
            fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf8');
            console.log(`Saved ${file}`);
        }
    }
    console.log(`Done. Enriched ${totalEnriched} records.`);
}

main();
