package me.iacn.bilineat.ui;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.ComponentName;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.preference.Preference;
import android.preference.SwitchPreference;
import android.widget.Toast;

import me.iacn.bilineat.BuildConfig;
import me.iacn.bilineat.R;
import me.iacn.bilineat.net.GetAdaptedTask;
import moe.feng.alipay.zerosdk.AlipayZeroSdk;

/**
 * Created by iAcn on 2016/10/28
 * Emali iAcn0301@foxmail.com
 */

public class AboutFragment extends BasePrefFragment {

    private PackageManager mManager;
    private ComponentName mComponentName;
    private SharedPreferences mSharedPref;

    @Override
    protected int getXmlId() {
        return R.xml.preference_about;
    }

    @Override
    protected void initPreference() {
        mManager = getActivity().getPackageManager();
        mComponentName = new ComponentName(getActivity(), MainActivity.class.getName() + "-Alias");
        mSharedPref = getActivity().getSharedPreferences("setting", Context.MODE_WORLD_READABLE);

        findPreference("version").setSummary(BuildConfig.VERSION_NAME);
        findPreference("donate").setOnPreferenceClickListener(new Preference.OnPreferenceClickListener() {
            @Override
            public boolean onPreferenceClick(Preference preference) {
                openAliPay();
                return true;
            }
        });

        SwitchPreference hideLauncher = (SwitchPreference) findPreference("hide_launcher");
        hideLauncher.setPersistent(false);
        hideLauncher.setOnPreferenceChangeListener(new Preference.OnPreferenceChangeListener() {
            @Override
            public boolean onPreferenceChange(Preference preference, Object newValue) {
                boolean value = (boolean) newValue;

                int state = value ? PackageManager.COMPONENT_ENABLED_STATE_DISABLED :
                        PackageManager.COMPONENT_ENABLED_STATE_ENABLED;

                mManager.setComponentEnabledSetting(mComponentName, state,
                        PackageManager.DONT_KILL_APP);

                mSharedPref.edit().putBoolean("change_method_executed", true).apply();

                return true;
            }
        });

        boolean isHide = mManager.getComponentEnabledSetting(mComponentName) ==
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED;

        boolean executed = mSharedPref.getBoolean("change_method_executed", false);

        hideLauncher.setChecked(!executed || isHide);

        new GetAdaptedTask(findPreference("adapted")).execute();
    }

    private void openAliPay() {
        if (AlipayZeroSdk.hasInstalledAlipayClient(getActivity())) {
            AlipayZeroSdk.startAlipayClient(getActivity(), "aex03925j2gcc9fv5imib0c");
        } else {
            copyToClipboard("895081850@qq.com");
            Toast.makeText(getActivity(),
                    "未安装支付宝客户端\n已将支付宝ID复制到剪贴板", Toast.LENGTH_SHORT).show();
        }
    }

    private void copyToClipboard(String str) {
        ClipboardManager manager = (ClipboardManager) getActivity()
                .getSystemService(Context.CLIPBOARD_SERVICE);

        manager.setPrimaryClip(ClipData.newPlainText(null, str));
    }
}