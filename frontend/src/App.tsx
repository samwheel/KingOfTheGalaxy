import { useState, useEffect } from "react";
import type { Star } from "./Star"
import type {Empire} from "./empire"
import Starmap from "./starmap"
import StarView from "./StarView"

function App() {
    const [selectedStar, setSelectedStar] = useState<Star | null>(null);
    const [empires, setEmpires] = useState<Empire[]>([])

    useEffect(() => {
        let isCancelled = false;

        // Fetch empires and starmap together so we can find which star
        // contains the first planet returned by the API.
        Promise.all([
            fetch("/empires").then((response) => {
                if (!response.ok) throw new Error(`Request failed: ${response.status}`);
                return response.json();
            }),
            fetch("/starmap").then((response) => {
                if (!response.ok) throw new Error(`Request failed: ${response.status}`);
                return response.json();
            }),
        ])
            .then(([empiresResult, starmap]) => {
                if (isCancelled) return;
                setEmpires(empiresResult);

                // Find the star that owns the first planet (if present)
                if (Array.isArray(empiresResult) && empiresResult.length > 0 && Array.isArray(empiresResult[0].planets) && empiresResult[0].planets.length > 0) {
                    const firstPlanetName = empiresResult[0].planets[0];
                    const foundStar = Array.isArray(starmap) ? (starmap as Star[]).find((s) => Array.isArray(s.planets) && s.planets.includes(firstPlanetName)) : undefined;
                    setSelectedStar(foundStar ?? null);
                } else {
                    setSelectedStar(null);
                }
            })
            .catch((error) => {
                console.error("Error fetching empires or starmap:", error);
            });

        return () => {
            isCancelled = true;
        };
    }, [])

    return (
        <>
            <Starmap setSelectedStar={setSelectedStar} empires={empires} selectedStar={selectedStar} />
            {selectedStar && <StarView star={selectedStar} empires={empires} />}
        </>
    )
}

export default App