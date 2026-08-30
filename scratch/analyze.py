from bs4 import BeautifulSoup

def analyze():
    html = open('d:/GenAI/Practice/RAG_UC/scratch_html.html', 'r', encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')

    def find_context(text):
        node = soup.find(string=lambda t: t and text in t)
        if node:
            parent = node.parent
            print(f'Text: {text}')
            print(f'Parent Tag: {parent.name}, Class: {parent.get("class")}')
            # Walk up a bit
            for i in range(3):
                parent = parent.parent
                if parent:
                    print(f'  Ancestor {i+1}: {parent.name}, Class: {parent.get("class")}')
        else:
            print(f'Text: {text} not found')
        print('-'*40)

    find_context('NAV')
    find_context('Expense Ratio')
    find_context('AUM')
    find_context('Holdings')
    find_context('Fund Manager')

if __name__ == "__main__":
    analyze()
