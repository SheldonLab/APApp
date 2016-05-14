package randolph.apphysicsapplication;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.view.View.OnClickListener;
import android.widget.Toast;

import com.loopj.android.http.*;
import org.json.*;

import java.io.IOException;
import java.io.UnsupportedEncodingException;

import cz.msebera.android.httpclient.Header;
import cz.msebera.android.httpclient.HttpEntity;
import cz.msebera.android.httpclient.NoHttpResponseException;
import cz.msebera.android.httpclient.client.ClientProtocolException;
import cz.msebera.android.httpclient.client.HttpRequestRetryHandler;
import cz.msebera.android.httpclient.entity.StringEntity;
import cz.msebera.android.httpclient.message.BasicHeader;
import cz.msebera.android.httpclient.params.HttpProtocolParams;
import cz.msebera.android.httpclient.protocol.HTTP;
import cz.msebera.android.httpclient.protocol.HttpContext;


public class MainActivity extends AppCompatActivity {

    Object obj1a;
    Object obj1b;
    Object obj2;
    EditText numberBox;
    EditText initialsBox;
    Context context;
    Intent successIntent;
    Intent failIntent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        context = this.getApplication();

        successIntent = new Intent(this,success.class);
        failIntent = new Intent(this, fail.class);


        //List 1a
        Spinner spinner1a = (Spinner) findViewById(R.id.spinner1a);
        ArrayAdapter<CharSequence> adapter1a = ArrayAdapter.createFromResource(this,
                R.array.list1a_array, android.R.layout.simple_spinner_item);
        adapter1a.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner1a.setAdapter(adapter1a);

        spinner1a.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                obj1a = parent.getItemAtPosition(pos);
            }

            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        //List 1b
        Spinner spinner1b = (Spinner) findViewById(R.id.spinner1b);
        ArrayAdapter<CharSequence> adapter1b = ArrayAdapter.createFromResource(this,
                R.array.list1b_array, android.R.layout.simple_spinner_item);
        adapter1b.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner1b.setAdapter(adapter1b);

        spinner1b.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                obj1b = parent.getItemAtPosition(pos);
            }

            public void onNothingSelected(AdapterView<?> parent) {
            }
        });


        //List 2
        Spinner spinner2 = (Spinner) findViewById(R.id.spinner2);
        ArrayAdapter<CharSequence> adapter2 = ArrayAdapter.createFromResource(this,
                R.array.list2_array, android.R.layout.simple_spinner_item);
        adapter2.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner2.setAdapter(adapter2);
        spinner2.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            public void onItemSelected(AdapterView<?> parent, View view, int pos, long id) {
                obj2 = parent.getItemAtPosition(pos);
            }

            public void onNothingSelected(AdapterView<?> parent) {
            }
        });


        //send button
        Button sendButton = (Button) findViewById(R.id.button);
        sendButton.setOnClickListener(sendListener);

        //initials field
        initialsBox = (EditText) findViewById(R.id.editText);
        numberBox = (EditText) findViewById(R.id.editText2);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }


    private OnClickListener sendListener = new OnClickListener() {
        public void onClick(View v) {
            String item1 = obj1a.toString() + '-' + obj1b.toString();
            String item2 = obj2.toString();
            String initials = initialsBox.getText().toString();
            String number = numberBox.getText().toString();
            JSONObject params = new JSONObject();
            StringEntity entity = null;
            try {
                params.put("item1", item1);
                params.put("item2", item2);
                params.put("initials", initials);
                params.put("number", number);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            try {
                entity = new StringEntity(params.toString());
                entity.setContentType(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
            AsyncHttpClient client = new AsyncHttpClient();
            client.setMaxRetriesAndTimeout(2, 2000);
            client.post(context, "http://52.91.240.90:8000/data", entity, "application/json", new AsyncHttpResponseHandler() {
                        @Override
                        public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                            stopService(successIntent);
                            startService(successIntent);
                        }

                        @Override
                        public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                            stopService(failIntent);
                            startService(failIntent);
                        }
                    }
            );


        }
    };

}
