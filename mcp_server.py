"""
MCP Server for Cardiac Total Peripheral Resistance Index (TPRI) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import TotalPeripheralResistanceClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cardiac-total-peripheral-resistance-tpri-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_hemodynamics",
                        "description": "Calculate SVR, TPRI, MAP, and cardiac index to assess vascular tone and afterload.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "systolic_bp_mmhg": {"type": "number", "description": "Systolic Blood Pressure (mmHg)."},
                                "diastolic_bp_mmhg": {"type": "number", "description": "Diastolic Blood Pressure (mmHg)."},
                                "cardiac_output_l_min": {"type": "number", "description": "Cardiac output (L/min)."},
                                "central_venous_pressure_mmhg": {"type": "number", "description": "CVP in mmHg (default: 4.0)."},
                                "height_cm": {"type": "number", "description": "Height in cm (default: 175.0)."},
                                "weight_kg": {"type": "number", "description": "Weight in kg (default: 70.0)."}
                            },
                            "required": ["systolic_bp_mmhg", "diastolic_bp_mmhg", "cardiac_output_l_min"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_hemodynamics":
            client = TotalPeripheralResistanceClient()
            try:
                res = client.evaluate_hemodynamics(
                    systolic_bp_mmhg=float(args["systolic_bp_mmhg"]),
                    diastolic_bp_mmhg=float(args["diastolic_bp_mmhg"]),
                    cardiac_output_l_min=float(args["cardiac_output_l_min"]),
                    central_venous_pressure_mmhg=float(args.get("central_venous_pressure_mmhg", 4.0)),
                    height_cm=float(args.get("height_cm", 175.0)),
                    weight_kg=float(args.get("weight_kg", 70.0))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
