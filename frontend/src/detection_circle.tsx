import colorStringToHex from "./string_to_hex"

export default function DetectionCircle(props: { radius: number, color: string }) {
    const diameter = props.radius * 2

    return (
        <svg
            className="detection-circle"
            width={diameter}
            height={diameter}
            viewBox={`0 0 ${diameter} ${diameter}`}
            style={{
                position: "absolute",
                left: "50%",
                top: "50%",
                transform: "translate(-50%, -50%) scale(0.8333333333)",
            }}
            aria-hidden="true"
        >
            <circle
                cx={props.radius}
                cy={props.radius}
                r={Math.max(0, props.radius - 1)}
                fill={colorStringToHex(props.color) + "04"}
                stroke={colorStringToHex(props.color) + "40"}
                strokeWidth="2"
            />
        </svg>
    )
}