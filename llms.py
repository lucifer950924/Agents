from langchain_ollama import ChatOllama
import asyncio, tracemalloc

class OllamaLLM:
    def __init__(self, model:str = "phi3:mini"):
        self.model = model
        self.llm = ChatOllama(model=self.model)

    
    async def call(self, prompt:str):
        return await self.llm.ainvoke(prompt)
        


async def main():
    tracemalloc.start()
    model = OllamaLLM()

    prompts = ['Who is Harry Potter?','What is AI?','What is the role of ethics in ai?']

    semaphore = asyncio.Semaphore(len(prompts))

    async with semaphore:
        response = await asyncio.gather(*[model.call(x) for x in prompts])

    print(response)


if __name__ == "__main__":
    asyncio.run(main())

