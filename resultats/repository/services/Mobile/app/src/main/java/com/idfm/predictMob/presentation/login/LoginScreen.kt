package com.idfm.predictMob.presentation.login

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Login
import androidx.compose.material.icons.filled.DirectionsCar
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Login
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.idfm.predictMob.R
import com.idfm.predictMob.ui.theme.PredicMobTheme






@Composable
fun LoginScreen(
    onLoginSuccess: () -> Unit,
) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(PredicMobTheme.color.White)
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Logo
            Icon(
                painter = painterResource(id = R.drawable.idfm),
                contentDescription = "Logo",
                tint =  PredicMobTheme.color.Blue,
                modifier = Modifier.size(150.dp)
            )

            Text(
                text = "Bienvenue",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = PredicMobTheme.color.Blue
            )

            Text(
                text = "Connectez-vous pour suivre votre\nmobilité",
                fontSize = 14.sp,
                color = PredicMobTheme.color.Blue.copy(alpha = 0.7f),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Google Login Button
            Button(
                onClick = { onLoginSuccess()},
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PredicMobTheme.color.BlueDark
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Login,
                    contentDescription = null,
                    tint = PredicMobTheme.color.Blue,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Continuer avec SSO", color = Color.White)
            }


            Text(
                text = "ou",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.2f),
                fontSize = 14.sp
            )

            // Email Input
            OutlinedTextField(
                value = "",
                onValueChange = { },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("Adresse e-mail") },
                leadingIcon = {
                    Icon(Icons.Default.Email, contentDescription = null, tint = Color.White.copy(alpha = 0.5f))
                },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = PredicMobTheme.color.Blue,
                    unfocusedBorderColor = PredicMobTheme.color.Blue.copy(alpha = 0.3f),
                    focusedTextColor = PredicMobTheme.color.Blue,
                    unfocusedTextColor = PredicMobTheme.color.Blue
                ),
                shape = RoundedCornerShape(12.dp)
            )

            // Password Input
            OutlinedTextField(
                value = "",
                onValueChange = { },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("Mot de passe") },
                leadingIcon = {
                    Icon(Icons.Default.Lock, contentDescription = null, tint = Color.White.copy(alpha = 0.5f))
                },
                trailingIcon = {
                    Icon(Icons.Default.VisibilityOff, contentDescription = null, tint = Color.White.copy(alpha = 0.5f))
                },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = PredicMobTheme.color.Blue,
                    unfocusedBorderColor = PredicMobTheme.color.Blue.copy(alpha = 0.3f),
                    focusedTextColor = PredicMobTheme.color.Blue,
                    unfocusedTextColor = PredicMobTheme.color.Blue
                ),
                shape = RoundedCornerShape(12.dp)
            )

            Text(
                text = "Mot de passe oublié ?",
                color = PredicMobTheme.color.Blue.copy(alpha = 0.7f),
                fontSize = 14.sp,
                modifier = Modifier.align(Alignment.End)
            )

            // Login Button
            Button(
                onClick = {onLoginSuccess() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = PredicMobTheme.color.Blue
                ),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Se connecter", color = PredicMobTheme.color.White, fontWeight = FontWeight.Bold)
            }

            Row {
                Text("Première visite ? ", color = PredicMobTheme.color.Blue.copy(alpha = 0.7f), fontSize = 14.sp)
                Text("Créez un compte", color = PredicMobTheme.color.Blue, fontSize = 14.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}


@Preview(showBackground = true)
@Composable
fun LoginScreenPreview() {
    LoginScreen({})
}