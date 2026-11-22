# pstack model configuration (CommandCode Go Plan)

# Per-role model overrides for pstack skills on CommandCode under the $1/mo Go plan.
# Designed around CommandCode's $10 shared monthly pool ($3/5h, $6/7d limits)
# and the models documented at https://commandcode.ai/docs/plans/go.

# 1. Core Logic & Architecture (Deep reasoning, bounded token cost)
bug-fix: DeepSeek V4 Pro
perf-issue: DeepSeek V4 Pro
hillclimb: DeepSeek V4 Pro
architect: Qwen 4 Max
judgment and prose: DeepSeek V4 Pro
strongest judgment: Qwen 4 Max

# 2. Fast Implementation & Swarm Workers (Ultra-low token cost: ~$0.10 - $0.16/1M)
feature, refactoring: DeepSeek V4.1 Flash Fast
swarm workers: Qwen 3.8 Flash
no-comments reviewer: DeepSeek V4.1 Flash Fast

# 3. Multi-Model Adversarial Panels (True cross-family diversity from the Go catalog)
# Arena races across DeepSeek, Qwen, GPT-Luna, and Mistral
arena runners: DeepSeek V4 Pro, Qwen 4 Max, GPT-6 Luna, Mistral Large 4
arena cross-judge pool: Qwen 4 Max, DeepSeek V4 Pro, Mistral Large 4
interrogate reviewers: DeepSeek V4 Pro, Qwen 4 Max, GPT-6 Luna
thermos reviewers: DeepSeek V4 Pro, Qwen 4 Max

# 4. Zero-Cost Fallback
# When nearing the $3/5hr usage limit, switch workers to Flint (free, 262K context)
fallback free model: Flint

session hook: on
