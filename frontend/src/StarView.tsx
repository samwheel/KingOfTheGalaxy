import { useEffect, useState } from "react";
import type { Star } from "./Star";
import "./StarView.scss";
import type { Planet } from "./planet";
import type { Empire } from "./empire"

export default function StarView(props: {star: Star; empires: Empire[]}) {
    const { star } = props;
    const [planets, setPlanets] = useState<Planet[]>([]);

    useEffect(() => {
        if (!star) {
            setPlanets([]);
            return;
        }

        let isCancelled = false;

        fetch(`/starmap/${encodeURIComponent(star.name)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Request failed: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (!isCancelled) {
                    

                    setPlanets(data.planets);
                }
            })
            .catch(error => {
                console.error("Error fetching star data:", error);
                if (!isCancelled) {
                    setPlanets([]);
                }
            });

        return () => {
            isCancelled = true;
        };
    }, [star?.name]);

    const planets_to_colors: Record<string, string> = {}
    for(let empire of props.empires) {
        for(let planet of empire.planets) {
            planets_to_colors[planet] = empire.color
        }   
    }

    const starColor = star.planets
        .map((planet) => planets_to_colors[planet])
        .find((color) => Boolean(color)) ?? "white";

    return (
        <div className="star-view">
            <h2 style={{ color: starColor }}>{star.name}</h2>
            <ul>
                {planets.map((planet, index) => {
                    const planetColor = planets_to_colors[planet.name] ?? "white";

                    return (
                        <div className="planet" key={index} style={{ color: planetColor }}>
                            <h3>{planet.name}</h3>
                            <ul>
                                <li>Environment: {planet.environment}</li>
                                <li>Population: {planet.population}</li>
                                <li>
                                    <h4>Statistics:</h4>
                                    <ul>
                                        <li>Population: {planet.statistics.population}</li>
                                        <li>GDP: {planet.statistics.GDP}</li>
                                        <li>Research: {planet.statistics.research}</li>
                                        <li>Defense: {planet.statistics.defense}</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    );
                })}
            </ul>
        </div>
    )
}