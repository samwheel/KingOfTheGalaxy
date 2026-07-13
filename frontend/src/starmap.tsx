import { useEffect, useState, type PointerEvent as ReactPointerEvent } from "react"
import type { Star } from "./Star"
import "./starmap.scss"

export default function Starmap() {
    const [starmap, setStarmap] = useState<Star[]>([])
    const [viewOffset, setViewOffset] = useState({ x: 0, y: 0 })
    const [dragState, setDragState] = useState<{ x: number; y: number; offsetX: number; offsetY: number } | null>(null)
    const [zoomLevel, setZoomLevel] = useState(1)
    const coordinateScale = 10

    useEffect(() => {
        fetch("http://127.0.0.1:5000/starmap")
            .then((response) => response.json())
            .then((data) => setStarmap(data))
            .catch((error) => console.error("Error fetching starmap:", error))
    }, [])

    const handlePointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
        event.preventDefault()
        setDragState({
            x: event.clientX,
            y: event.clientY,
            offsetX: viewOffset.x,
            offsetY: viewOffset.y,
        })
        event.currentTarget.setPointerCapture(event.pointerId)
    }

    const handlePointerMove = (event: ReactPointerEvent<HTMLDivElement>) => {
        if (!dragState) {
            return
        }

        const deltaX = Math.round(event.clientX - dragState.x)
        const deltaY = Math.round(event.clientY - dragState.y)

        setViewOffset({
            x: dragState.offsetX + deltaX / (zoomLevel * coordinateScale),
            y: dragState.offsetY + deltaY / (zoomLevel * coordinateScale),
        })
    }

    const handlePointerUp = (event: ReactPointerEvent<HTMLDivElement>) => {
        if (event.currentTarget.hasPointerCapture(event.pointerId)) {
            event.currentTarget.releasePointerCapture(event.pointerId)
        }
        setDragState(null)
    }

    const handleScroll = (event: React.WheelEvent<HTMLDivElement>) => {
        event.preventDefault()

        const rect = event.currentTarget.getBoundingClientRect()
        const mouseX = event.clientX - rect.left
        const mouseY = event.clientY - rect.top
        const zoomFactor = 0.1
        const nextZoomLevel = Math.max(0.1, Math.min(zoomLevel - event.deltaY * zoomFactor * 0.01, 10))

        if (nextZoomLevel === zoomLevel) {
            return
        }

        const worldX = mouseX / (zoomLevel * coordinateScale) - viewOffset.x
        const worldY = mouseY / (zoomLevel * coordinateScale) - viewOffset.y

        setViewOffset({
            x: mouseX / (nextZoomLevel * coordinateScale) - worldX,
            y: mouseY / (nextZoomLevel * coordinateScale) - worldY,
        })
        setZoomLevel(nextZoomLevel)
    }

    return (
        <div
            className={`starmap ${dragState ? "dragging" : ""}`}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={handlePointerUp}
            onPointerCancel={handlePointerUp}
            onLostPointerCapture={handlePointerUp}
            onWheel={handleScroll}
        >
            <h2>Starmap</h2>
            {starmap.map((star, index) => (
                <div key={index} className="star" style={{ left: `${(star.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale}px`, top: `${(star.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale}px` }}>
                    <div className="star-container">
                        <div className="star-background"></div>
                        <h3 className="star-name">{star.name}</h3>
                    </div>
                </div>
            ))}
            {starmap.map((star, index) => (
                star.star_lane_connections.map((connectedStar, connectionIndex) => {
                    const connectedStarData = starmap.find(s => s.name === connectedStar)
                    if (!connectedStarData) return null

                    const x1 = (star.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale
                    const y1 = (star.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale - 17
                    const x2 = (connectedStarData.coordinates[0] + viewOffset.x) * zoomLevel * coordinateScale
                    const y2 = (connectedStarData.coordinates[1] + viewOffset.y) * zoomLevel * coordinateScale - 17

                    return (
                        <svg key={`${index}-${connectionIndex}`} className="star-connection" style={{ position: "absolute", left: 0, top: 0, width: "100%", height: "100%" }}>
                            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="white" strokeWidth="1" />
                        </svg>
                    )
                })
            ))}
        </div>
    )
}