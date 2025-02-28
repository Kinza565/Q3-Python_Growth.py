import streamlite as st
import panadas as pd
import os
from io import BytesIo

st.set_page_config(page_title="Data Sweeper",layout="wide" )


#custom css
st.markdown(
    """
<style>
.stApp{
background-color: black;
color: white
}
</style>

""",
unsafe_allow_hml=True
    )

#title and description

st.title("Datasweeper sterling Integrator By Kinzah Khan")
st.markdown("Transform your files between CSV and Excel format with built-in data cleaning and visualization creating the project for quarter3!")

#file upload

uploaded_file = st.file_uploader("upload your files (accepts CVS or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)

        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            continue

        #file details
st.write("preview the head of te Dataframe")
st.dataframe(df.head())

#data cleaning options
st.write("Select the cleaning options you want to apply")
if st.checkbox(f"clean data foe {file.name}"):
    coll, coll2 = st.columns(2)

    with coll:
        if st.button(f"Remove duplicate from the file : {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("Duplicates removed")
            with coll2:
                if st.button(f"Remove duplicate from the file : {file.name}"):
                    numeric_cols =  df.select_dtypes(includes=["numeric"]).columns
                    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.filename(x.median()))
                    st.write("Missing values have been filled")

                    st.subheader("select Columns to Keep")
                    columns = st.multiselect(f"choose columns for {file.name}", df.columns, default=df.columns)
                    df = df[columns]

#data visualization

st.subheader("Data visualization")

if st.checkbox(f"Show Visualize data for {file.name}"):
    st.bar_chart(df.select_dtypes(include= "number").iloc[:, :2])

#converter Options

st.subheader("Conversion Options")
conversion_type = st.radio(f"Convert {file.name} to:", ["CVS" , "Excel"], key=file.name)
if st.button(f"Convert{file.name}"):
    buffer = BytesIo()
    if conversion_type == "CSV":
        df.to_csv(buffer, index=False)
        file.name = file.name.replace(file_ext, "csv")
        mime_type = "text/csv"


    elif conversion_type == "Excel":
        df.to.to_excel(buffer, index=False)
        file.name = file.name.replace(file_ext, "xlsx")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)


        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file.name,
            mimetype=mime_type
        )

        st.success("All Files Processed Successfully")
        
    

