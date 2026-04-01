from fastapi import APIRouter
from app.converters import get_registry

router = APIRouter(prefix="/api", tags=["formats"])


@router.get("/formats")
async def get_all_formats():
    """Get all supported formats grouped by category."""
    registry = get_registry()
    return registry.get_supported_formats()


@router.get("/formats/{input_format}")
async def get_output_formats(input_format: str):
    """Get all possible output formats for a given input format."""
    registry = get_registry()
    result = registry.get_output_formats_for(input_format)
    if not result:
        return {"error": f"No conversions available for .{input_format}", "formats": {}}
    return {"formats": result}


@router.get("/formats-list")
async def get_formats_list():
    """Get flat lists of all input and output formats."""
    registry = get_registry()
    return {
        "input": registry.get_all_input_formats(),
        "output": registry.get_all_output_formats(),
    }
