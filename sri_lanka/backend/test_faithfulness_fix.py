"""
Quick test script to verify the faithfulness check fix works locally
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, '/home/ranga/code/pragith/whatssapp-chat/supermarket-rag/backend')

async def test_faithfulness_check():
    from rag_engine import rag_engine
    from llama_index.llms.litellm import LiteLLM
    from llama_index.core.schema import TextNode, NodeWithScore
    
    # Create a test LLM instance
    test_llm = LiteLLM(
        model="openai/gemini-2.0-flash",
        api_key=rag_engine.master_key,
        api_base=rag_engine.litellm_api_base,
        temperature=0.1
    )
    
    # Create mock context nodes with ice cream data
    mock_nodes = [
        NodeWithScore(
            node=TextNode(
                text="Peters Drumstick Ice Cream 4 Pack $6.50 SAVE $2.00 WAS $8.50",
                metadata={"shop_name": "Coles", "page": 1}
            ),
            score=0.9
        ),
        NodeWithScore(
            node=TextNode(
                text="Peters Ice Cream Variety Pack 8 Pack $10.00 Special Offer",
                metadata={"shop_name": "Woolworths", "page": 2}
            ),
            score=0.85
        )
    ]
    
    # Test response that should pass
    test_response = """
| Product | Store | Price | Deal |
|---|---|---|---|
| Peters Drumstick Ice Cream 4 Pack | Coles | $6.50 | SAVE $2.00 |
| Peters Ice Cream Variety Pack 8 Pack | Woolworths | $10.00 | Special Offer |

**Verdict**: Coles has the better deal for the Drumstick 4 Pack at $6.50 with $2 savings.

---
*I compare deals from mall catalogues and may miss the latest updates. Deals may be expired or unavailable at the store's discretion. This is for educational purposes only.*
"""
    
    print("Testing faithfulness check with ice cream price comparison...")
    print(f"Mock context: {len(mock_nodes)} nodes with ice cream data")
    print(f"Test response length: {len(test_response)} chars")
    
    is_faithful = await rag_engine._check_output_faithfulness(
        test_response,
        mock_nodes,
        test_llm
    )
    
    print(f"\nFaithfulness Check Result: {'PASSED ✅' if is_faithful else 'FAILED ❌'}")
    
    if is_faithful:
        print("SUCCESS: The fix allows valid ice cream price comparisons to pass!")
        return True
    else:
        print("FAILURE: The check is still too strict")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_faithfulness_check())
    sys.exit(0 if result else 1)
"""
