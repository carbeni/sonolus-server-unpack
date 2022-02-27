import argparse
from unpack import Unpacker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Unpack resources from Sonolus servers.'
    )
    parser.add_argument(
        '-s', '--server', help='Server base url.', required=True
    )
    parser.add_argument(
        '-o', '--output', help='Output directory.', default="source/"
    )
    parser.add_argument(
        '-v', "--verbose", action="store_true", help='Display messages.'
    )
    subparsers = parser.add_subparsers(help="Resource type.")
    parser_level = subparsers.add_parser('level', help='Unpack a level.')
    parser_level.add_argument('level_name', type=str, help='Level name.')
    parser_level = subparsers.add_parser('skin', help='Unpack a skin.')
    parser_level.add_argument('skin_name', type=str, help='Skin name.')
    parser_level = subparsers.add_parser('bg', help='Unpack a background.')
    parser_level.add_argument('bg_name', type=str, help='Background name.')
    parser_level = subparsers.add_parser('effect', help='Unpack a effect.')
    parser_level.add_argument('effect_name', type=str, help='Effect name.')
    parser_level = subparsers.add_parser('particle', help='Unpack a particle.')
    parser_level.add_argument('particle_name', type=str, help='Particle name.')
    parser_level = subparsers.add_parser('engine', help='Unpack a engine.')
    parser_level.add_argument('engine_name', type=str, help='Engine name.')
    parser_level.add_argument(
        '-r', "--recursive", action="store_true", help='Unpacks engine resources recursively.'
    )

    args = parser.parse_args()

    u = Unpacker(args.server, args.output, args.verbose)
    if hasattr(args, "level_name"):
        u.unpack_level(args.level_name)
    if hasattr(args, "skin_name"):
        u.unpack_level(args.skin_name)
    if hasattr(args, "bg_name"):
        u.unpack_background(args.bg_name)
    if hasattr(args, "effect_name"):
        u.unpack_effect(args.effect_name)
    if hasattr(args, "particle_name"):
        u.unpack_particle(args.particle_name)
    if hasattr(args, "engine_name"):
        u.unpack_engine(
            args.engine_name, is_recursive=args.recursive
        )
