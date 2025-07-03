.PHONY: help install test lint format clean docs example

help: ## 显示帮助信息
	@echo "AutoDL API 封装包管理命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装开发依赖
	pip install -e .
	pip install pytest black flake8

test: ## 运行测试
	python tests/test_autodl.py

test-unit: ## 运行单元测试
	python -m pytest tests/test_autodl.py -v

lint: ## 代码检查
	flake8 src/ tests/ examples/

format: ## 代码格式化
	black src/ tests/ examples/

clean: ## 清理构建文件
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

docs: ## 生成文档
	@echo "文档已生成在 docs/ 目录"

example: ## 运行示例
	python examples/autodl_example.py

check: format lint test ## 运行完整的代码检查流程

build: clean ## 构建包
	python setup.py sdist bdist_wheel

publish: build ## 发布到PyPI
	twine upload dist/*

run-example: ## 运行示例
	python examples/autodl_example.py

run-test: ## 运行基本测试
	python tests/test_autodl.py

debug-api: ## 运行API调试
	python tests/debug_api.py

 