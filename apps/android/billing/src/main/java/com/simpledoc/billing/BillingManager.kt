package com.simpledoc.billing

import android.app.Activity
import com.android.billingclient.api.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Manages Google Play Billing v6 subscriptions.
 * 
 * Products:
 * - Monthly: ₹149/mo (product_id: "simpledoc_monthly")
 * - Yearly: ₹999/yr (product_id: "simpledoc_yearly")
 * 
 * TODO: Implement Play Billing Library integration
 * TODO: Handle subscription states (active, expired, grace period)
 * TODO: Implement referral unlock (7-day trial)
 */
class BillingManager(
    private val activity: Activity
) : PurchasesUpdatedListener, BillingClientStateListener {
    
    private lateinit var billingClient: BillingClient
    
    private val _subscriptionState = MutableStateFlow<SubscriptionState>(SubscriptionState.Unknown)
    val subscriptionState: StateFlow<SubscriptionState> = _subscriptionState.asStateFlow()
    
    private val _isPremium = MutableStateFlow(false)
    val isPremium: StateFlow<Boolean> = _isPremium.asStateFlow()
    
    companion object {
        const val PRODUCT_MONTHLY = "simpledoc_monthly"
        const val PRODUCT_YEARLY = "simpledoc_yearly"
    }
    
    fun initialize() {
        billingClient = BillingClient.newBuilder(activity)
            .setListener(this)
            .enablePendingPurchases()
            .build()
        
        billingClient.startConnection(this)
    }
    
    /**
     * Check if user has active subscription.
     */
    fun hasActiveSubscription(): Boolean {
        // TODO: Query purchases and check subscription status
        return _isPremium.value
    }
    
    /**
     * Launch subscription purchase flow.
     */
    fun purchaseSubscription(productId: String) {
        // TODO: Launch billing flow
        // val productDetailsParams = ProductDetailsParams.newBuilder()
        //     .setProductDetails(productDetails)
        //     .build()
        // billingClient.launchBillingFlow(activity, billingFlowParams)
    }
    
    /**
     * Unlock premium via referral code (7-day trial).
     */
    fun unlockReferralTrial(referralCode: String) {
        // TODO: Validate referral code server-side
        // TODO: Grant 7-day premium access
    }
    
    override fun onPurchasesUpdated(billingResult: BillingResult, purchases: List<Purchase>?) {
        // TODO: Handle purchase updates
    }
    
    override fun onBillingSetupFinished(billingResult: BillingResult) {
        if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
            // TODO: Query purchases
        }
    }
    
    override fun onBillingServiceDisconnected() {
        // TODO: Retry connection
    }
}

sealed class SubscriptionState {
    object Unknown : SubscriptionState()
    object Free : SubscriptionState()
    data class Premium(val productId: String, val expiryDate: Long) : SubscriptionState()
    object Expired : SubscriptionState()
}

