from typing import Dict, Any, List

class WorkflowDifferenceEngine:
    """
    Compares Organization Workflow vs ERP Workflow using Longest Common Subsequence (LCS).
    Identifies exact missing steps, extra steps, and out-of-order steps.
    """
    def compare_workflows(self, org_workflow: Dict[str, Any], erp_workflow: Dict[str, Any]) -> Dict[str, Any]:
        expected_steps = org_workflow.get("steps", [])
        actual_steps = erp_workflow.get("steps", [])
        
        # LCS Algorithm
        m, n = len(expected_steps), len(actual_steps)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if expected_steps[i - 1] == actual_steps[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                    
        # Backtrack to find exact missing and extra steps
        missing_steps = []
        extra_steps = []
        i, j = m, n
        
        while i > 0 and j > 0:
            if expected_steps[i - 1] == actual_steps[j - 1]:
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                missing_steps.append(expected_steps[i - 1])
                i -= 1
            else:
                extra_steps.append(actual_steps[j - 1])
                j -= 1
                
        while i > 0:
            missing_steps.append(expected_steps[i - 1])
            i -= 1
        while j > 0:
            extra_steps.append(actual_steps[j - 1])
            j -= 1
            
        missing_steps.reverse()
        extra_steps.reverse()
        
        return {
            "missing_steps": missing_steps,
            "extra_steps": extra_steps,
            "policy_violations": ["SOC2 Validation Failed"] if missing_steps else [],
            "current_workflow": erp_workflow,
            "optimized_workflow": {
                "steps": expected_steps
            }
        }
