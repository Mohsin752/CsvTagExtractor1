import streamlit as st
import pandas as pd
import io
from tag_processor import TagProcessor

def main():
    st.set_page_config(
        page_title="CSV Tag Extractor - SEO Edition",
        page_icon="🏷️",
        layout="wide"
    )

    st.title("🏷️ CSV Tag Extractor - SEO Edition")
    st.write("Upload your CSV file and extract SEO-optimized tags from selected columns.")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)

            # Display basic file info
            st.write(f"File uploaded successfully! Shape: {df.shape}")

            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())

            # Column selection
            st.subheader("Tag Extraction Settings")

            col1, col2 = st.columns(2)

            with col1:
                selected_columns = st.multiselect(
                    "Select columns for tag extraction",
                    options=df.columns.tolist(),
                    help="Choose one or more columns containing tags"
                )

            with col2:
                delimiter = st.text_input(
                    "Tag delimiter",
                    value=",",
                    help="Character used to separate tags in the selected columns"
                )

            if selected_columns:
                # Process button
                if st.button("Extract SEO Tags", type="primary"):
                    # Create a progress bar
                    progress_bar = st.progress(0)

                    # Dictionary to store results
                    results = {}

                    # Process each selected column and add new columns with extracted tags
                    for idx, column in enumerate(selected_columns):
                        result_dict = TagProcessor.process_column(df, column, delimiter)
                        results[column] = result_dict['tags']

                        # Create new columns with extracted tags and meta descriptions
                        base_name = column.replace(' ', '_').lower()

                        # Column for SEO-optimized tags
                        seo_tags_col = f"{base_name}_seo_tags"
                        df[seo_tags_col] = df[column].apply(
                            lambda x: TagProcessor.format_seo_tags(
                                TagProcessor.extract_tags(str(x), delimiter)
                            ) if pd.notna(x) else ""
                        )

                        # Column for meta descriptions
                        meta_desc_col = f"{base_name}_meta_description"
                        df[meta_desc_col] = df[column].apply(
                            lambda x: TagProcessor.create_meta_description(
                                TagProcessor.extract_tags(str(x), delimiter)
                            ) if pd.notna(x) else ""
                        )

                        progress_bar.progress((idx + 1) / len(selected_columns))

                    # Display results
                    st.subheader("Extracted SEO Tags")

                    for column, tags in results.items():
                        with st.expander(f"SEO Tags from {column} ({len(tags)} unique keywords)"):
                            st.write("### Primary Keywords")
                            st.write(", ".join(tags[:10]))
                            st.write("### Long-tail Keywords")
                            st.write(", ".join(tags[10:30]))

                    # Show updated dataframe
                    st.subheader("Updated Dataset with SEO Tags")
                    st.dataframe(df)

                    # Create CSV download button
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)

                    st.download_button(
                        label="Download SEO-Enhanced CSV",
                        data=csv_buffer.getvalue(),
                        file_name="seo_enhanced_dataset.csv",
                        mime="text/csv"
                    )

                    # Prepare text download data
                    download_data = "# SEO-Optimized Tags Report\n\n"
                    for column, tags in results.items():
                        download_data += f"## Tags from {column}\n"
                        download_data += "### Primary Keywords\n"
                        download_data += ", ".join(tags[:10]) + "\n\n"
                        download_data += "### Long-tail Keywords\n"
                        download_data += ", ".join(tags[10:30]) + "\n\n"
                        download_data += "### All Keywords\n"
                        download_data += "\n".join(tags) + "\n\n"

                    # Create text download button for tags only
                    st.download_button(
                        label="Download SEO Report",
                        data=download_data,
                        file_name="seo_tags_report.txt",
                        mime="text/plain"
                    )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.write("Please make sure your CSV file is properly formatted and try again.")

    # Add useful information at the bottom
    with st.expander("ℹ️ How to use"):
        st.write("""
        1. Upload a CSV file using the file uploader above
        2. Select one or more columns containing tags
        3. Specify the delimiter used to separate tags in your data
        4. Click 'Extract SEO Tags' to process the data
        5. View and download:
           - SEO-enhanced CSV with new tag columns and meta descriptions
           - Detailed SEO report with primary and long-tail keywords

        The SEO enhancement includes:
        - Semantic variations of tags
        - Meta descriptions for each row
        - Primary and long-tail keyword organization
        - SEO-friendly formatting
        """)

if __name__ == "__main__":
    main()