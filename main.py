from src.swap import V1Swap
import asyncio

async def main():
    # Example usage
    v1_swap = V1Swap()
    await v1_swap.v1_swap()


if __name__ == "__main__":
    asyncio.run(main())