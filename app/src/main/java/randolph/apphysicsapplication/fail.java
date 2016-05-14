package randolph.apphysicsapplication;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.widget.Toast;

/**
 * Created by bradley on 12/30/15.
 */
public class fail extends Service {

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public void onCreate(){
        Toast.makeText(this, "Data did not upload, check internet connection", Toast.LENGTH_LONG).show();
    }
}
