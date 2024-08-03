import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline

def display_text_box_title_only(title):
    st.markdown(
        f"""
        <div style="border: 1px solid #cccccc; border-radius: 5px; overflow: hidden;">
            <div style="background-color: #f0f0f0; padding: 10px;">
                <p style="margin: 0; color: black; font-weight: bold; font-size: 1.0em; padding: 0;">{title}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def display_text_box(title, content):
    st.markdown(
        f"""
        <div style="border: 1px solid #cccccc; border-radius: 5px; overflow: hidden;">
            <div style="background-color: #f0f0f0; padding: 10px;">
                <p style="margin: 0; color: black; font-weight: bold; font-size: 1.0em; padding: 0;">{title}</p>
            </div>
            <div style="padding: 10px; background-color: white;">
                <p>{content}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def display_eating_habits():
    st.write('')
    st.write('')
    title4 = "DESCRIPTIVE ANALYSIS"
    display_text_box_title_only(title4)
    st.write("### Correlation Analysis")
    st.write('')

    # Explanation about the correlation coefficient
    explanation = """
    The correlation coefficient measures the strength and direction of the linear relationship between two variables. 
    It ranges from -1 to 1:
    - 1 indicates a perfect positive relationship, where as one variable increases, the other also increases proportionally.
    - -1 indicates a perfect negative relationship, where as one variable increases, the other decreases proportionally.
    - 0 indicates no linear relationship between the variables.
    """
    st.write(explanation)

    # Load data and define columns to encode
    df = pd.read_csv('obesity.csv')
    X = df.drop(columns=['NObeyesdad'])
    target_variable = 'NObeyesdad'

    # Original feature names
    original_feature_names = list(X.columns)

    # Define columns to encode
    binary_cols = ['Gender', 'family_history_with_overweight', 'SMOKE', 'SCC', 'FAVC']
    ordinal_cols = ['CALC', 'CAEC']
    onehot_cols = ['MTRANS']
    round_cols = ["FCVC", "NCP", "CH2O", "TUE", "FAF"]  # Columns to be rounded

    # Define preprocessing pipelines
    binary_pipeline = Pipeline(steps=[('label_encoder', OrdinalEncoder())])
    ordinal_pipeline = Pipeline(steps=[('ordinal_encoder', OrdinalEncoder(categories=[['no', 'Sometimes', 'Frequently', 'Always']] * 2))])
    scaler_pipeline = Pipeline(steps=[('scaler', MinMaxScaler())])

    # Apply ordinal and binary encoding
    binary_encoded = binary_pipeline.fit_transform(X[binary_cols])
    ordinal_encoded = ordinal_pipeline.fit_transform(X[ordinal_cols])

    # Round specified columns to integers
    X[round_cols] = X[round_cols].round().astype(int)

    # Create DataFrame with encoded features
    df_encoded = pd.DataFrame(binary_encoded, columns=binary_cols)
    df_encoded[ordinal_cols] = ordinal_encoded

    # One-hot encode the MTRANS column using pandas get_dummies
    mtrans_encoded = pd.get_dummies(X[onehot_cols[0]], prefix='MTRANS')

    # Scale remaining columns
    remaining_cols = [col for col in original_feature_names if col not in binary_cols + ordinal_cols + onehot_cols]
    remaining_scaled = scaler_pipeline.fit_transform(X[remaining_cols])

    # Combine all preprocessed features
    df_remaining_scaled = pd.DataFrame(remaining_scaled, columns=remaining_cols)
    df_preprocessed = pd.concat([df_encoded, mtrans_encoded, df_remaining_scaled], axis=1)

    # Encode target variable
    categories = [['Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I',
                   'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']]
    encoder = OrdinalEncoder(categories=categories)
    y = encoder.fit_transform(df[[target_variable]])

    # Create DataFrame with preprocessed features and target variable using original names
    df_preprocessed[target_variable] = y

    # Mapping for feature names
    feature_name_mapping = {col: col for col in df_preprocessed.columns}
    reverse_feature_name_mapping = {v: k for k, v in feature_name_mapping.items()}
    readable_features = [feature_name_mapping[col] for col in df_preprocessed.columns if col != 'NObeyesdad']

    # Define mapping for ordinal features
    ordinal_mappings = {
        'FCVC': {1: 'Never', 2: 'Sometimes', 3: 'Always'},
        'NCP': {1: 'Between 1 and 2', 2: 'Three', 3: 'More than three'},
        'CH2O': {1: 'Less than a liter', 2: 'Between 1 and 2 L', 3: 'More than 2 L'},
        'FAF': {0: 'I do not have', 1: '1 or 2 days', 2: '2 or 4 days', 3: '4 or 5 days'},
        'TUE': {0: '0-2 hours', 1: '3-5 hours', 2: 'More than 5 hours'}
    }


    # Correlation Analysis
    st.write("### Correlation Analysis")
    col1, col2 = st.columns([1, 3])

    with col1:
        st.write("**Obesity Level**")
    with col2:
        selected_readable_feature = st.selectbox("Select a feature to see its correlation with Obesity Level", readable_features)

    # Get the preprocessed feature name from the readable name
    selected_feature = reverse_feature_name_mapping[selected_readable_feature]

    # Ensure the selected feature and target variable are numeric
    if pd.api.types.is_numeric_dtype(df_preprocessed[selected_feature]) and pd.api.types.is_numeric_dtype(df_preprocessed['NObeyesdad']):
        # Calculate and display correlation
        correlation = df_preprocessed[selected_feature].corr(df_preprocessed['NObeyesdad'])
        st.write(f"Correlation between {selected_readable_feature} and Obesity Level: {correlation:.2f}")

        # Display correlation matrix if the user selects a feature
        if selected_feature:
            # Create the correlation matrix
            corr_matrix = df_preprocessed[[selected_feature, 'NObeyesdad']].corr()

            # Display the correlation matrix
            fig, ax = plt.subplots()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
            ax.set_title(f'Correlation Heatmap')
            st.pyplot(fig)
    else:
        st.write("Selected feature or target variable is not numeric, unable to compute correlation.")

    # Distribution Analysis
    st.write("### Distribution Analysis")
    st.write("Select a feature to see its distribution across different Obesity Levels:")
    selected_feature_dist = st.selectbox("Select feature for distribution analysis", [feat for feat in readable_features if feat not in ['Age', 'Height', 'Weight']])

    # Plot distribution if a feature is selected
    if selected_feature_dist:
        # Use the raw data for distribution analysis, rounding specific columns
        X[round_cols] = X[round_cols].round().astype(int)

        # Plotting
        fig_dist = plt.figure(figsize=(12, 8))

        if selected_feature_dist in ordinal_mappings:
            order = list(ordinal_mappings[selected_feature_dist].keys())
            labels = list(ordinal_mappings[selected_feature_dist].values())
            sns.countplot(data=X, x=selected_feature_dist, hue=df[target_variable], palette='husl', order=order)
            plt.xlabel(selected_feature_dist)
            plt.xticks(range(len(order)), labels)  # Set xticks to match labels
        else:
            sns.countplot(data=X, x=selected_feature_dist, hue=df[target_variable], palette='husl')
            plt.xlabel(selected_feature_dist)

        plt.title(f'Distribution of {selected_feature_dist} Across Obesity Levels')
        plt.ylabel('Count')
        plt.legend(title='Obesity Level', loc='upper right', labels=categories[0])
        plt.xticks(rotation=45)
        st.pyplot(fig_dist)

    #Display countplot for the obesity levels
    st.write("### Which Weight Level Is The Most Prevalent?")
    fig_target = plt.figure(figsize=(12, 8))
    sns.countplot(data=df, x=target_variable, palette='husl')
    plt.title("Weight Category Counts: Target Variable")
    plt.xlabel("Obesity Level")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig_target)

display_eating_habits()