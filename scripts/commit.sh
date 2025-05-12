#!/bin/bash

echo "🚀 Initiating magic pre-commit sequence..."

echo "🤔 What kind of change are you committing?"
select opt in "✨ Feature" "🐛 Bugfix" "🚑 Hotfix" "🚀 Improvement" "📝 Documentation" "♻️ Refactor" "💄 Style" "✅ Test" "🔨 Chore"; do
  case $REPLY in
    1)
      commitType="✨ feat"
      break
      ;;
    2)
      commitType="🐛 fix"
      break
      ;;
    3)
      commitType="🚑 hotfix"
      break
      ;;
    4)
      commitType="🚀 improvement"
      break
      ;;
    5)
      commitType="📝 docs"
      break
      ;;
    6)
      commitType="♻️ refactor"
      break
      ;;
    7)
      commitType="💄 style"
      break
      ;;
    8)
      commitType="✅ test"
      break
      ;;
    9)
      commitType="🔨 chore"
      break
      ;;
    *) echo "🤯 That's not a valid option. Try again?" ;;
  esac
done

echo "📜 Please type your commit message:"
read commitMessage

if [ -z "$commitMessage" ]; then
  echo "❌ A commit without a message is like a spell without an incantation. Please try again."
  exit 1
fi

magicCommitMessage="$commitType: $commitMessage"

echo "🧹 Cleaning comments from code files..."
python3 ./scripts/clean_comments.py
if [ $? -ne 0 ]; then
  echo "⚠️ Issues detected while cleaning comments. Please check the output above."
else
  echo "✨ Comments cleaned successfully!"
fi

echo "🧹 Running code formatters on all supported file types..."
./scripts/format_code.sh
if [ $? -ne 0 ]; then
  echo "⚠️ Code formatting issues detected. Please fix them before committing."
  echo "   Run ./scripts/format_code.sh manually to see detailed errors."
else
  echo "✨ All code files are beautifully formatted!"
fi 

echo "🔥 Removing all __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "✅ All __pycache__ directories removed!"

echo "🧙‍♂️ Gathering all your changes..."
git add .

echo "🔮 Sealing your changes with a spell: '$magicCommitMessage'"
git commit -m "$magicCommitMessage"
echo "🎉 Ta-da! Your changes are now a part of history!"
