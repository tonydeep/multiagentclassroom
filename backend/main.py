"""
FastAPI backend for Multi-Agent Classroom.

A professional implementation using FastAPI with WebSocket support
for real-time multi-agent conversations powered by Claude Agent SDK.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.api.routes import problems_router, sessions_router
from backend.api.websocket.manager import manager
from backend.services.dialogue_service import process_user_message, cleanup_session
from backend.models import MessageCreate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Multi-Agent Classroom - FastAPI Backend")
    logger.info("=" * 60)

    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        logger.warning("⚠️  ANTHROPIC_API_KEY not found in environment!")
        logger.warning("Please set it in your .env file")

    logger.info("✓ FastAPI server starting...")
    logger.info("✓ WebSocket support enabled")
    logger.info("✓ Claude Agent SDK integrated")

    yield

    # Shutdown
    logger.info("Shutting down server...")


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Classroom API",
    description="Real-time multi-agent learning environment powered by Claude Agent SDK",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(problems_router)
app.include_router(sessions_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Multi-Agent Classroom API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv('ANTHROPIC_API_KEY'))
    }


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time communication.

    Args:
        websocket: WebSocket connection
        session_id: Session identifier
    """
    await manager.connect(websocket, session_id)

    try:
        # Send connection confirmation
        await manager.send_personal_message(
            {"type": "connected", "data": {"session_id": session_id}},
            websocket
        )

        logger.info(f"WebSocket connected for session: {session_id}")

        # Listen for messages
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "send_message":
                # User sent a message
                message_data = data.get("data", {})
                sender_name = message_data.get("sender_name", "Student")
                message_text = message_data.get("message", "")

                logger.info(f"Received message from {sender_name}: {message_text}")

                # Process the message
                try:
                    result = await process_user_message(
                        session_id=session_id,
                        sender_name=sender_name,
                        message_text=message_text
                    )

                    if result:
                        logger.info(f"Agent {result['agent']} responded")
                    else:
                        logger.warning("No agent response generated")

                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await manager.send_error(session_id, str(e))

            elif message_type == "end_session":
                # Client requested to end session
                cleanup_session(session_id)
                await manager.send_system_status(
                    session_id,
                    "Phiên học đã kết thúc"
                )
                break

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session: {session_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        manager.disconnect(websocket, session_id)


if __name__ == "__main__":
    import uvicorn

    logger.info("\n" + "=" * 60)
    logger.info("Starting FastAPI server...")
    logger.info("Server will be available at: http://localhost:8000")
    logger.info("API documentation at: http://localhost:8000/docs")
    logger.info("=" * 60 + "\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
