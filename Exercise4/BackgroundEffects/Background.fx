sampler tex : register(s0);

float4 Font( float2 uv: TEXCOORD0, float4 color : COLOR0 ) : COLOR 
{
    return tex2D(tex, uv) * float4(uv.y, 1, uv.y, 1);
}

technique FontEffect
{
    pass P0
    {
        PixelShader  = compile ps_2_0 Font();
    }
}
