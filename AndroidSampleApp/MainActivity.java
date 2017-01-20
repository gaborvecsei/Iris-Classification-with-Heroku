package com.gabor.vecsei.irisclassification;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    Button sendButton;
    EditText dataInput1;
    EditText dataInput2;
    EditText dataInput3;
    EditText dataInput4;
    ImageView imgView;
    String predictionUrl = "http://iris-classifier-example.herokuapp.com/predict";
    String isModelLoadedUrl = "http://iris-classifier-example.herokuapp.com/isModelLoaded";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sendButton = (Button) findViewById(R.id.send_button);
        imgView = (ImageView) findViewById(R.id.chart_image_view);
        dataInput1 = (EditText) findViewById(R.id.data_input1);
        dataInput2 = (EditText) findViewById(R.id.data_input2);
        dataInput3 = (EditText) findViewById(R.id.data_input3);
        dataInput4 = (EditText) findViewById(R.id.data_input4);

        new CheckModelLoader(isModelLoadedUrl).execute();

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), InputMethodManager.RESULT_UNCHANGED_SHOWN);
                String data = dataInput1.getText().toString() + "-" +
                        dataInput2.getText().toString() + "-" +
                        dataInput3.getText().toString() + "-" +
                        dataInput4.getText().toString();
                if (dataInput1.getText().toString().equals("") || dataInput2.getText().toString().equals("") || dataInput3.getText().toString().equals("") || dataInput4.getText().toString().equals("")) {
                    Toast.makeText(MainActivity.this, "Please fill every value!", Toast.LENGTH_SHORT).show();
                } else {
                    new IrisPrediction(predictionUrl, MainActivity.this).execute(data);
                }
            }
        });
    }

    class Iris {

        String b64Img;
        String name;
        float accuracy;

        Iris(String name, float accuracy, String b64Img) {
            this.b64Img = b64Img;
            this.name = name;
            this.accuracy = accuracy;
        }
    }

    class IrisPrediction extends AsyncTask<String, Void, Iris> {

        private String baseUrl;
        private ProgressDialog progressDialog;

        public IrisPrediction(String baseUrl, Activity activity) {
            this.baseUrl = baseUrl;
            progressDialog = new ProgressDialog(activity);
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog.setMessage("Thinking...");
            progressDialog.show();
        }

        @Override
        protected Iris doInBackground(String... params) {
            String res = getResults(params[0]);

            JSONObject dataJson;
            Iris iris = null;
            try {
                dataJson = new JSONObject(res);
                iris = new Iris(dataJson.getString("prediction_label"), Float.valueOf(dataJson.getString("accuracy")), dataJson.getString("prediction_bar_chart"));
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return iris;
        }

        @Override
        protected void onPostExecute(Iris iris) {
            // Visualize the base64 image about the prediction
            progressDialog.dismiss();
            super.onPostExecute(iris);
            String b64ImgStr = iris.b64Img;
            Bitmap bm = base64ToBitmap(b64ImgStr);
            imgView.setImageBitmap(Bitmap.createScaledBitmap(bm, imgView.getWidth(), imgView.getHeight(), false));
        }

        private Bitmap base64ToBitmap(String base64Str) {
            // Convert base64 String to Bitmap image
            byte[] decodedString = Base64.decode(base64Str, Base64.DEFAULT);
            return BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        }

        private String getResults(String data) {
            String response = "";
            String link = baseUrl + "/" + data;
            HttpURLConnection conn;
            try {
                URL url = new URL(link);
                conn = (HttpURLConnection) url.openConnection();
                conn.connect();

                InputStream is = conn.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                String line = "";

                while ((line = reader.readLine()) != null) {
                    response += line;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            return response;
        }
    }

    class CheckModelLoader extends AsyncTask<Void, Void, Void> {

        private String baseUrl;

        public CheckModelLoader(String baseUrl) {
            this.baseUrl = baseUrl;
        }

        @Override
        protected Void doInBackground(Void... params) {
            HttpURLConnection conn;
            try {
                URL url = new URL(baseUrl);
                conn = (HttpURLConnection) url.openConnection();
                conn.connect();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
