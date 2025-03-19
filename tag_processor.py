import pandas as pd
import re
from typing import List, Set, Dict
import string

class TagProcessor:
    @staticmethod
    def clean_tag(tag: str) -> str:
        """Clean and normalize a single tag."""
        # Convert to lowercase and remove special characters
        tag = tag.lower().strip()
        tag = re.sub(r'[^\w\s-]', '', tag)
        # Replace multiple spaces with single space
        tag = re.sub(r'\s+', ' ', tag)
        return tag

    @staticmethod
    def generate_seo_variations(tag: str) -> Set[str]:
        """Generate SEO-friendly variations of a tag."""
        tag = tag.strip()
        variations = set()

        # Add original tag
        variations.add(tag)

        # Add without spaces
        if ' ' in tag:
            variations.add(tag.replace(' ', ''))
            variations.add(tag.replace(' ', '-'))

        # Add plural/singular forms (basic)
        if tag.endswith('s'):
            variations.add(tag[:-1])
        else:
            variations.add(tag + 's')

        return variations

    @staticmethod
    def create_meta_description(tags: Set[str]) -> str:
        """Create an SEO-friendly meta description from tags."""
        tag_list = sorted(list(tags))
        if not tag_list:
            return ""

        description = f"Featuring {', '.join(tag_list[:3])}"
        if len(tag_list) > 3:
            description += f" and {len(tag_list)-3} more topics"
        return description

    @staticmethod
    def extract_tags(text: str, delimiter: str = ',') -> Set[str]:
        """Extract tags from text using specified delimiter."""
        if not isinstance(text, str):
            return set()

        # Split text by delimiter and clean each tag
        tags = text.split(delimiter)
        base_tags = {TagProcessor.clean_tag(tag) for tag in tags if tag.strip()}

        # Generate SEO variations for each tag
        seo_tags = set()
        for tag in base_tags:
            seo_tags.update(TagProcessor.generate_seo_variations(tag))

        # Remove empty strings
        seo_tags.discard('')
        return seo_tags

    @staticmethod
    def process_column(df: pd.DataFrame, column_name: str, delimiter: str = ',') -> Dict[str, List[str]]:
        """Process a column and extract unique tags with SEO enhancements."""
        all_tags = set()
        meta_descriptions = []

        # Process each non-null value in the column
        for value in df[column_name].dropna():
            row_tags = TagProcessor.extract_tags(str(value), delimiter)
            all_tags.update(row_tags)
            meta_descriptions.append(TagProcessor.create_meta_description(row_tags))

        return {
            'tags': sorted(list(all_tags)),
            'meta_descriptions': meta_descriptions
        }

    @staticmethod
    def format_seo_tags(tags: Set[str]) -> str:
        """Format tags in an SEO-friendly string format."""
        if not tags:
            return ""
        return ", ".join(sorted(tags)) + f" | {len(tags)} relevant keywords"