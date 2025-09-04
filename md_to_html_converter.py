#!/usr/bin/env python3
"""
SEO-Optimized Markdown to HTML Converter
Converts markdown files to HTML with comprehensive SEO elements for better Google indexing
"""

import re
import sys
import os
from datetime import datetime
import urllib.parse

def extract_paper_info(markdown_content):
    """Extract paper information from markdown content"""
    paper_info = {
        'title': '',
        'authors': '',
        'journal': '',
        'published': '',
        'doi': '',
        'url': ''
    }
    
    # Extract paper title
    title_match = re.search(r'\*\*Paper:\*\*\s*\[([^\]]+)\]\(([^)]+)\)', markdown_content)
    if title_match:
        paper_info['title'] = title_match.group(1)
        paper_info['url'] = title_match.group(2)
    
    # Extract authors
    authors_match = re.search(r'\*\*Authors:\*\*\s*(.+?)(?:\n|$)', markdown_content)
    if authors_match:
        paper_info['authors'] = authors_match.group(1).strip()
    
    # Extract journal (optional)
    journal_match = re.search(r'\*\*Journal:\*\*\s*(.+?)(?:\n|$)', markdown_content)
    if journal_match:
        paper_info['journal'] = journal_match.group(1).strip()
    
    # Extract published date (optional)
    published_match = re.search(r'\*\*Published:\*\*\s*(.+?)(?:\n|$)', markdown_content)
    if published_match:
        paper_info['published'] = published_match.group(1).strip()
    
    # Extract DOI
    doi_match = re.search(r'\*\*DOI:\*\*\s*(.+?)(?:\n|$)', markdown_content)
    if doi_match:
        paper_info['doi'] = doi_match.group(1).strip()
    
    return paper_info

def generate_seo_meta_tags(title, description, keywords, author="Siyang Liu", domain="https://lsy641.github.io"):
    """Generate comprehensive SEO meta tags"""
    
    # Extract filename for URL
    filename = title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
    url = f"{domain}/notes/{filename}.html"
    
    meta_tags = f"""
    <!-- SEO Meta Tags -->
    <meta name="description" content="{description}" />
    <meta name="keywords" content="{keywords}" />
    <meta name="author" content="{author}" />
    <meta name="robots" content="index, follow" />
    <meta name="language" content="English" />
    <meta name="revisit-after" content="7 days" />
    
    <!-- Open Graph Meta Tags for Social Media -->
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{domain}/images/robotics-notes.jpg" />
    <meta property="og:site_name" content="Siyang Liu's Academic Website" />
    <meta property="og:locale" content="en_US" />
    <meta property="article:author" content="{author}" />
    <meta property="article:published_time" content="{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}" />
    <meta property="article:modified_time" content="{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}" />
    <meta property="article:section" content="Research Notes" />
    <meta property="article:tag" content="{keywords.split(',')[0]}" />
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{domain}/images/robotics-notes.jpg" />
    <meta name="twitter:creator" content="@siyang_liu" />
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{url}" />
    
    <!-- Academic Profile Links -->
    <link rel="author" href="https://scholar.google.com/citations?user=2OjUAPUAAAAJ" />
    
    <!-- Navigation Links -->
    <link rel="up" href="{domain}/research-notes.html" />
    <link rel="home" href="{domain}/" />
    """
    
    return meta_tags

def generate_structured_data(title, description, paper_info, author="Siyang Liu", domain="https://lsy641.github.io"):
    """Generate structured data (JSON-LD) for SEO"""
    
    filename = title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
    url = f"{domain}/notes/{filename}.html"
    
    # Extract topics from description
    topics = ["AI in Robotics", "Research Notes", "Academic Analysis"]
    if "lifelong learning" in description.lower():
        topics.append("Lifelong Learning")
    if "sim-to-real" in description.lower():
        topics.append("Sim-to-Real Transfer")
    if "human-robot" in description.lower():
        topics.append("Human-Robot Interaction")
    
    structured_data = f"""
    <!-- Structured Data for Article -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "image": "{domain}/images/robotics-notes.jpg",
        "author": {{
            "@type": "Person",
            "name": "{author}",
            "url": "{domain}/",
            "jobTitle": "Ph.D. Student in Computer Engineering",
            "worksFor": {{
                "@type": "Organization",
                "name": "University of Michigan"
            }},
            "sameAs": [
                "https://scholar.google.com/citations?user=2OjUAPUAAAAJ"
            ]
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "{author}'s Academic Website",
            "url": "{domain}/"
        }},
        "datePublished": "{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}",
        "dateModified": "{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{url}"
        }},
        "about": [
            {", ".join([f'{{"@type": "Thing", "name": "{topic}"}}' for topic in topics])}
        ],
        "keywords": "{description}",
        "articleSection": "Research Notes",
        "inLanguage": "en",
        "isPartOf": {{
            "@type": "CollectionPage",
            "name": "Research Notes",
            "url": "{domain}/research-notes.html"
        }}"""
    
    # Add paper mention if available
    if paper_info.get('title'):
        structured_data += f""",
        "mentions": [
            {{
                "@type": "ScholarlyArticle",
                "name": "{paper_info['title']}",
                "url": "{paper_info.get('url', '')}",
                "author": {{
                    "@type": "Person",
                    "name": "{paper_info.get('authors', 'Unknown')}"
                }},
                "publisher": {{
                    "@type": "Organization",
                    "name": "{paper_info.get('journal', 'Unknown')}"
                }},
                "datePublished": "{paper_info.get('published', '')}"
            }}
        ]"""
    
    structured_data += """
    }
    </script>
    
    <!-- Additional Structured Data for Breadcrumb -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://lsy641.github.io/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Research Notes",
                "item": "https://lsy641.github.io/research-notes.html"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "Reading Notes",
                "item": "https://lsy641.github.io/notes/"
            }
        ]
    }
    </script>
    """
    
    return structured_data

def generate_css():
    """Generate comprehensive CSS for the HTML"""
    return """
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f8f9fa;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h1 { font-size: 2.2em; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { font-size: 1.8em; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }
        h3 { font-size: 1.4em; }
        h4 { font-size: 1.2em; }
        p { margin-bottom: 15px; }
        ul, ol { margin-bottom: 15px; padding-left: 30px; }
        li { margin-bottom: 5px; }
        
        /* Nested list styling */
        ul ul, ol ul, ul ol, ol ol {
            margin-top: 10px;
            margin-bottom: 10px;
            padding-left: 20px;
        }
        
        /* Make nested lists visually distinct */
        li > ul, li > ol {
            margin-top: 8px;
            margin-bottom: 8px;
        }
        
        /* Style for list items with nested content */
        li:has(ul), li:has(ol) {
            margin-bottom: 15px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        pre code {
            background: none;
            padding: 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            color: #555;
            font-style: italic;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        strong { font-weight: bold; }
        em { font-style: italic; }
        hr {
            border: none;
            border-top: 1px solid #bdc3c7;
            margin: 30px 0;
        }
        .paper-meta {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .note-info {
            background-color: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }
        .breadcrumb {
            background-color: #f8f9fa;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
        .breadcrumb a {
            color: #666;
        }
        .breadcrumb a:hover {
            color: #3498db;
        }
        .navigation {
            margin: 20px 0;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        .navigation a {
            margin-right: 15px;
            padding: 8px 15px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.2s ease;
        }
        .navigation a:hover {
            background-color: #2980b9;
            transform: translateY(-1px);
        }
        article {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            margin: 20px 0;
        }
        header {
            margin-bottom: 30px;
        }
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }
    </style>
    """

def markdown_to_html(markdown_content, title="Document", author="Siyang Liu", domain="https://lsy641.github.io"):
    """Convert markdown content to SEO-optimized HTML"""
    
    # Extract paper information
    paper_info = extract_paper_info(markdown_content)
    
    # Generate description from content
    lines = markdown_content.split('\n')
    description = ""
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('**') and len(line.strip()) > 20:
            description = line.strip()[:200] + "..." if len(line.strip()) > 200 else line.strip()
            break
    
    # Generate keywords
    keywords = "AI in robotics, embodied AI, robot learning, human-robot interaction, research notes, academic analysis"
    if "lifelong learning" in markdown_content.lower():
        keywords += ", lifelong learning"
    if "sim-to-real" in markdown_content.lower():
        keywords += ", sim-to-real transfer"
    if "data collection" in markdown_content.lower():
        keywords += ", data collection"
    if "generative models" in markdown_content.lower():
        keywords += ", generative models"
    
    # Generate meta tags and structured data
    meta_tags = generate_seo_meta_tags(title, description, keywords, author, domain)
    structured_data = generate_structured_data(title, description, paper_info, author, domain)
    css = generate_css()
    
    # Convert markdown to HTML
    html_content = markdown_content
    
    # Headers (skip H1 since we have it in the header)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    # Convert H1 to H2 to avoid duplication
    html_content = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    
    # Bold and italic
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Links with proper attributes
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" rel="noopener" target="_blank">\1</a>', html_content)
    
    # Code blocks
    html_content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # Lists - Enhanced approach for complex nested structures
    lines = html_content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Handle ordered lists (1. item)
        if re.match(r'^\d+\. ', line_stripped):
            processed_lines.append('<ol>')
            
            # Process all consecutive ordered list items
            while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
                content = re.sub(r'^\d+\. ', '', lines[i].strip())
                processed_lines.append(f'<li>{content}')
                
                # Look for nested content (indented with spaces)
                j = i + 1
                nested_content = []
                while j < len(lines) and lines[j].startswith('    ') and lines[j].strip().startswith('* '):
                    nested_item = lines[j].strip()[2:]  # Remove '* '
                    
                    # Collect all continuation lines for this nested item
                    nested_text = [nested_item]
                    k = j + 1
                    while k < len(lines) and lines[k].startswith('    ') and not lines[k].strip().startswith('* '):
                        nested_text.append(lines[k].strip())
                        k += 1
                    
                    # Join the nested content
                    complete_nested = ' '.join(nested_text)
                    nested_content.append(f'<li>{complete_nested}</li>')
                    j = k
                
                # Also look for any continuation text that belongs to the main list item
                continuation_text = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')) and not lines[j].strip().startswith('- ') and not lines[j].strip().startswith('##') and not lines[j].strip().startswith('###') and lines[j].strip() != '':
                    if not lines[j].startswith('    '):  # Not nested content
                        continuation_text.append(lines[j].strip())
                    j += 1
                
                if continuation_text:
                    # Add continuation text to the current list item
                    content += ' ' + ' '.join(continuation_text)
                    # Update the list item with the combined content
                    processed_lines[-1] = f'<li>{content}'
                
                if nested_content:
                    processed_lines.append('<ul>')
                    processed_lines.extend(nested_content)
                    processed_lines.append('</ul>')
                    i = j - 1  # Adjust index
                
                processed_lines.append('</li>')
                i += 1
            
            processed_lines.append('</ol>')
            continue
        
        # Handle unordered lists (- item)
        elif line_stripped.startswith('- '):
            processed_lines.append('<ul>')
            
            # Process all consecutive unordered list items
            while i < len(lines) and lines[i].strip().startswith('- '):
                content = lines[i].strip()[2:]  # Remove '- '
                processed_lines.append(f'<li>{content}</li>')
                i += 1
            
            processed_lines.append('</ul>')
            continue
        
        # Handle standalone indented bullet points (* item) - convert to paragraphs
        elif line.startswith('    ') and line_stripped.startswith('* '):
            content = line_stripped[2:]  # Remove '* '
            
            # Handle multi-line content for this bullet point
            full_content = [content]
            j = i + 1
            while j < len(lines) and lines[j].startswith('    ') and not lines[j].strip().startswith('* '):
                # This is continuation of the same bullet point
                full_content.append(lines[j].strip())
                j += 1
            
            # Join all content and create a single paragraph
            complete_content = ' '.join(full_content)
            processed_lines.append(f'<p>{complete_content}</p>')
            i = j  # Skip the lines we've already processed
            continue
        
        # Regular line
        else:
            processed_lines.append(line)
            i += 1
    
    html_content = '\n'.join(processed_lines)
    
    # Paragraphs
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line and not line.startswith('<') and not line.startswith('#'):
            lines[i] = f'<p>{line}</p>'
    html_content = '\n'.join(lines)
    
    # Horizontal rules
    html_content = re.sub(r'^---$', r'<hr>', html_content, flags=re.MULTILINE)
    
    # Blockquotes
    html_content = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)
    
    # Clean up multiple consecutive p tags
    html_content = re.sub(r'</p>\s*<p>', '\n', html_content)
    
    # Generate filename for URL
    filename = title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
    
    # Create the full HTML document
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {author}</title>
    {meta_tags}
    {structured_data}
    {css}
    <!-- MathJax for math rendering -->
    <script>
    window.MathJax = {{ tex: {{ inlineMath: [["$", "$"], ["\\(", "\\)"]], displayMath: [["$$","$$"], ["\\[","\\]"]] }}, options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }} }};
    </script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="{domain}/">Home</a> &gt; 
        <a href="{domain}/research-notes.html">Research Notes</a> &gt; 
        Reading Notes
    </nav>

    <!-- Navigation Links -->
    <div class="navigation">
        <a href="{domain}/">← Back to Home</a>
        <a href="{domain}/research-notes.html">← Back to Research Notes</a>
    </div>

    <article>

        {html_content}

        <footer>
            <hr>
            <p><em>Notes by {author} - Last updated: {datetime.now().strftime('%B %d, %Y')}</em></p>
            <p><strong>Author:</strong> <a href="{domain}/">{author}</a> | <strong>Google Scholar:</strong> <a href="https://scholar.google.com/citations?user=2OjUAPUAAAAJ" rel="noopener" target="_blank">Profile</a></p>
        </footer>
    </article>
</body>
</html>"""
    
    return html_doc

def convert_markdown_to_html(markdown_content):
    """Convert markdown content to HTML"""
    
    # Convert markdown to HTML
    html_content = markdown_content
    
    # Headers (skip H1 since we have it in the header)
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    # Convert H1 to H2 to avoid duplication
    html_content = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    
    # Bold and italic
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Links with proper attributes
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" rel="noopener" target="_blank">\1</a>', html_content)
    
    # Code blocks
    html_content = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)
    
    # Lists - Enhanced approach for complex nested structures
    lines = html_content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # Handle ordered lists (1. item)
        if re.match(r'^\d+\. ', line_stripped):
            processed_lines.append('<ol>')
            
            # Process all consecutive ordered list items
            while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
                content = re.sub(r'^\d+\. ', '', lines[i].strip())
                processed_lines.append(f'<li>{content}')
                
                # Look for nested content (indented with spaces)
                j = i + 1
                nested_content = []
                while j < len(lines) and lines[j].startswith('    ') and lines[j].strip().startswith('* '):
                    nested_item = lines[j].strip()[2:]  # Remove '* '
                    
                    # Collect all continuation lines for this nested item
                    nested_text = [nested_item]
                    k = j + 1
                    while k < len(lines) and lines[k].startswith('    ') and not lines[k].strip().startswith('* '):
                        nested_text.append(lines[k].strip())
                        k += 1
                    
                    # Join the nested content
                    complete_nested = ' '.join(nested_text)
                    nested_content.append(f'<li>{complete_nested}</li>')
                    j = k
                
                # Also look for any continuation text that belongs to the main list item
                continuation_text = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')) and not lines[j].strip().startswith('- ') and not lines[j].strip().startswith('##') and not lines[j].strip().startswith('###') and lines[j].strip() != '':
                    if not lines[j].startswith('    '):  # Not nested content
                        continuation_text.append(lines[j].strip())
                    j += 1
                
                if continuation_text:
                    # Add continuation text to the current list item
                    content += ' ' + ' '.join(continuation_text)
                    # Update the list item with the combined content
                    processed_lines[-1] = f'<li>{content}'
                
                if nested_content:
                    processed_lines.append('<ul>')
                    processed_lines.extend(nested_content)
                    processed_lines.append('</ul>')
                    i = j - 1  # Adjust index
                
                processed_lines.append('</li>')
                i += 1
            
            processed_lines.append('</ol>')
            continue
        
        # Handle unordered lists (- item)
        elif line_stripped.startswith('- '):
            processed_lines.append('<ul>')
            
            # Process all consecutive unordered list items
            while i < len(lines) and lines[i].strip().startswith('- '):
                content = lines[i].strip()[2:]  # Remove '- '
                processed_lines.append(f'<li>{content}</li>')
                i += 1
            
            processed_lines.append('</ul>')
            continue
        
        # Handle standalone indented bullet points (* item) - convert to paragraphs
        elif line.startswith('    ') and line_stripped.startswith('* '):
            content = line_stripped[2:]  # Remove '* '
            
            # Handle multi-line content for this bullet point
            full_content = [content]
            j = i + 1
            while j < len(lines) and lines[j].startswith('    ') and not lines[j].strip().startswith('* '):
                # This is continuation of the same bullet point
                full_content.append(lines[j].strip())
                j += 1
            
            # Join all content and create a single paragraph
            complete_content = ' '.join(full_content)
            processed_lines.append(f'<p>{complete_content}</p>')
            i = j  # Skip the lines we've already processed
            continue
        
        # Regular line
        else:
            processed_lines.append(line)
            i += 1
    
    html_content = '\n'.join(processed_lines)
    
    # Paragraphs
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line and not line.startswith('<') and not line.startswith('#'):
            lines[i] = f'<p>{line}</p>'
    html_content = '\n'.join(lines)
    
    # Horizontal rules
    html_content = re.sub(r'^---$', r'<hr>', html_content, flags=re.MULTILINE)
    
    # Blockquotes
    html_content = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)
    
    # Clean up multiple consecutive p tags
    html_content = re.sub(r'</p>\s*<p>', '\n', html_content)
    
    return html_content

def generate_html_content(markdown_content, title, description, keywords, author, paper_url=None, paper_title=None, paper_authors=None, paper_journal=None, paper_date=None, paper_doi=None):
    """Generate complete HTML content with modern styling"""
    
    # Convert markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    # Generate current date for meta tags
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    # Create filename for the note
    note_filename = title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '')
    
    # Build paper meta section separately to avoid nested f-string issues
    paper_meta_section = ""
    if any([paper_url, paper_title, paper_authors, paper_journal, paper_date, paper_doi]):
        paper_meta_section = f'''

<div class="paper-meta">
    {f'<strong>Paper:</strong> <a href="{paper_url}" rel="noopener" target="_blank">{paper_title}</a><br>' if paper_url and paper_title else ''}
    {f'<strong>Authors:</strong> {paper_authors}<br>' if paper_authors else ''}
    {f'<strong>Journal:</strong> {paper_journal}<br>' if paper_journal else ''}
    {f'<strong>Published:</strong> {paper_date}<br>' if paper_date else ''}
    {f'<strong>DOI:</strong> <a href="https://doi.org/{paper_doi}" rel="noopener" target="_blank">{paper_doi}</a><br>' if paper_doi else ''}
</div>'''
    
    # Generate HTML template with modern styling
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Research Notes | Siyang Liu | University of Michigan</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="{description}" />
    <meta name="keywords" content="{keywords}" />
    <meta name="author" content="{author}" />
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
    <meta name="language" content="en" />
    <meta name="revisit-after" content="7 days" />
    <meta name="distribution" content="global" />
    <meta name="rating" content="general" />
    
    <!-- Open Graph Meta Tags for Social Media -->
    <meta property="og:title" content="{title} - Research Notes | Siyang Liu" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://lsy641.github.io/notes/{note_filename}" />
    <meta property="og:image" content="https://lsy641.github.io/images/profile.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{title} Research Notes" />
    <meta property="og:site_name" content="Siyang Liu - Academic Website" />
    <meta property="og:locale" content="en_US" />
    <meta property="article:author" content="{author}" />
    <meta property="article:published_time" content="{current_date}" />
    <meta property="article:modified_time" content="{current_date}" />
    <meta property="article:section" content="Research Notes" />
    <meta property="article:tag" content="{keywords.split(', ')[:3]}" />
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description[:100]}..." />
    <meta name="twitter:image" content="https://lsy641.github.io/images/profile.jpg" />
    <meta name="twitter:creator" content="@liusiyang_641" />
    
    <!-- Canonical URL -->
    <link rel="canonical" href="https://lsy641.github.io/notes/{note_filename}" />
    
    <!-- Academic Profile Links -->
    <link rel="author" href="https://scholar.google.com/citations?user=2OjUAPUAAAAJ" />
    
    <!-- Navigation Links -->
    <link rel="up" href="https://lsy641.github.io/research-notes" />
    <link rel="home" href="https://lsy641.github.io/" />
    
    <!-- MathJax for math rendering -->
    <script>
    window.MathJax = {{ tex: {{ inlineMath: [["$", "$"], ["\\(", "\\)"]], displayMath: [["$$","$$"], ["\\[","\\]"]] }}, options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }} }};
    </script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <!-- Structured Data for Article -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{description}",
        "image": "https://lsy641.github.io/images/profile.jpg",
        "author": {{
            "@type": "Person",
            "name": "{author}",
            "url": "https://lsy641.github.io/",
            "jobTitle": "Ph.D. Student in Computer Engineering",
            "worksFor": {{
                "@type": "Organization",
                "name": "University of Michigan"
            }},
            "sameAs": [
                "https://scholar.google.com/citations?user=2OjUAPUAAAAJ"
            ]
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Siyang Liu's Academic Website",
            "url": "https://lsy641.github.io/"
        }},
        "datePublished": "{current_date}",
        "dateModified": "{current_date}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://lsy641.github.io/notes/{note_filename}"
        }},
        "about": [
            {{"@type": "Thing", "name": "Research Notes"}}, 
            {{"@type": "Thing", "name": "Academic Analysis"}},
            {{"@type": "Thing", "name": "Literature Review"}}
        ],
        "keywords": "{keywords}",
        "articleSection": "Research Notes",
        "inLanguage": "en",
        "isPartOf": {{
            "@type": "CollectionPage",
            "name": "Research Notes",
            "url": "https://lsy641.github.io/research-notes"
        }}
        {f', "mentions": [{{"@type": "ScholarlyArticle", "name": "{paper_title}", "url": "{paper_url}"}}]' if paper_url and paper_title else ''}
    }}
    </script>
    
    <!-- Additional Structured Data for Breadcrumb -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://lsy641.github.io/"
            }},
            {{
                "@type": "ListItem",
                "position": 2,
                "name": "Research Notes",
                "item": "https://lsy641.github.io/research-notes"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "Reading Notes",
                "item": "https://lsy641.github.io/notes/"
            }}
        ]
    }}
    </script>
    
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f8f9fa;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        h1 {{ font-size: 2.2em; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ font-size: 1.8em; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        h3 {{ font-size: 1.4em; }}
        h4 {{ font-size: 1.2em; }}
        p {{ margin-bottom: 15px; }}
        ul, ol {{ margin-bottom: 15px; padding-left: 30px; }}
        li {{ margin-bottom: 5px; }}
        
        /* Nested list styling */
        ul ul, ol ul, ul ol, ol ol {{
            margin-top: 10px;
            margin-bottom: 10px;
            padding-left: 20px;
        }}
        
        /* Make nested lists visually distinct */
        li > ul, li > ol {{
            margin-top: 8px;
            margin-bottom: 8px;
        }}
        
        /* Style for list items with nested content */
        li:has(ul), li:has(ol) {{
            margin-bottom: 15px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            color: #555;
            font-style: italic;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        strong {{ font-weight: bold; }}
        em {{ font-style: italic; }}
        hr {{
            border: none;
            border-top: 1px solid #bdc3c7;
            margin: 30px 0;
        }}
        .paper-meta {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .note-info {{
            background-color: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 0 5px 5px 0;
        }}
        .breadcrumb {{
            background-color: #f8f9fa;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 0px;
            font-size: 0.9em;
        }}
        .breadcrumb a {{
            color: #666;
        }}
        .breadcrumb a:hover {{
            color: #3498db;
        }}
        .navigation {{
            margin: 0 0;
            padding: 5px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 0px solid #e9ecef;
        }}
        .navigation a {{
            margin-right: 15px;
            padding: 8px 15px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.2s ease;
        }}
        .navigation a:hover {{
            background-color: #2980b9;
            transform: translateY(-1px);
        }}
        article {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            margin: 20px 0;
        }}
        header {{
            margin-bottom: 30px;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
    
</head>
<body>
    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="https://lsy641.github.io/">Home</a> &gt; 
        <a href="https://lsy641.github.io/research-notes">Research Notes</a> &gt; 
        Reading Notes
    </nav>

    <!-- Navigation Links -->
    <div class="navigation">
        <a href="https://lsy641.github.io/">← Back to Home</a>
        <a href="https://lsy641.github.io/research-notes">← Back to Research Notes</a>
    </div>

    <article>

        {html_content}

        <footer>
            <hr>
            <p><em>Notes by {author} - Last updated: {datetime.now().strftime("%B %d, %Y")}</em></p>
            <p><strong>Author:</strong> <a href="https://lsy641.github.io/">{author}</a> | <strong>Google Scholar:</strong> <a href="https://scholar.google.com/citations?user=2OjUAPUAAAAJ" rel="noopener" target="_blank">Profile</a></p>
        </footer>
    </article>
</body>
</html>'''
    
    return html_template

def convert_file(input_file, output_file=None, title=None, author="Siyang Liu", domain="https://lsy641.github.io"):
    """Convert a markdown file to SEO-optimized HTML"""
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
    
    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Determine output filename
    if output_file is None:
        output_file = input_file.replace('.md', '.html')
    
    # Determine title
    if title is None:
        # Try to extract title from the first H1 heading in the markdown
        title_match = re.search(r'^# (.+?)$', markdown_content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # Fallback to filename if no H1 heading found
            title = os.path.splitext(os.path.basename(input_file))[0]
            # Convert filename to title case
            title = title.replace('-', ' ').replace('_', ' ').title()
    
    # Extract paper information
    paper_info = extract_paper_info(markdown_content)
    
    # Generate description from content
    lines = markdown_content.split('\n')
    description = ""
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('**') and len(line.strip()) > 20:
            description = line.strip()[:200] + "..." if len(line.strip()) > 200 else line.strip()
            break
    
    # Generate keywords
    keywords = "research notes, academic analysis, literature review, academic research"
    if "ai" in markdown_content.lower():
        keywords += ", artificial intelligence"
    if "machine learning" in markdown_content.lower():
        keywords += ", machine learning"
    if "robotics" in markdown_content.lower():
        keywords += ", robotics"
    if "nlp" in markdown_content.lower() or "natural language" in markdown_content.lower():
        keywords += ", natural language processing"
    if "computer vision" in markdown_content.lower():
        keywords += ", computer vision"
    
    # Use the new modern HTML generation function
    html_content = generate_html_content(
        markdown_content, 
        title, 
        description, 
        keywords, 
        author,
        paper_info.get('url'),
        paper_info.get('title'),
        paper_info.get('authors'),
        paper_info.get('journal'),
        paper_info.get('published'),
        paper_info.get('doi')
    )
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully converted '{input_file}' to '{output_file}' with SEO optimization")
    return True

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python md_to_html_converter.py <input.md> [output.html] [title] [author] [domain]")
        print("Example: python md_to_html_converter.py notes.md output.html 'My Notes' 'Siyang Liu' 'https://lsy641.github.io'")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    title = sys.argv[3] if len(sys.argv) > 3 else None
    author = sys.argv[4] if len(sys.argv) > 4 else "Siyang Liu"
    domain = sys.argv[5] if len(sys.argv) > 5 else "https://lsy641.github.io"
    
    convert_file(input_file, output_file, title, author, domain)

if __name__ == "__main__":
    main()
